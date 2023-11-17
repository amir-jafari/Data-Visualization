import math
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.transforms as mpt

import librosa

import utils


def main():
    st.header("Audio Processing")
    st.divider()
    st.subheader("Step 1: Audio File Upload and Play")

    audio_process_lst = ['Display', 'Feature extraction', 'Spectrogram decomposition', 'Temporal segmentation']
    process_name = utils.sidebar(audio_process_lst)

    uploaded_file = st.file_uploader("Choose an audio file", type=['mp3', 'wav', 'ogg', 'flac'])

    if not uploaded_file:
        st.stop()

    y, sr = librosa.load(uploaded_file, mono=False)
    y_stereo = None
    is_stereo = False

    if y.ndim == 2: # means it's stereo instead of mono
        # Convert stereo to mono by averaging the channels
        y_stereo = y.copy()
        y = np.mean(y, axis=0)
        is_stereo = True

    # print(f'y_stereo.shape {y_stereo.shape if is_stereo else y_stereo} y.shape {y.shape}, sr {sr}')

    st.audio(y, format='audio/ogg', sample_rate=sr)

    duration = math.ceil(len(y) / sr)

    st.write(
        f"The total length of the audio file is: ***{duration} seconds***. "
        f"And It's ***{'stereo' if is_stereo else 'mono'}*** audio file"
    )

    if st.toggle('Choose a part (a duration) of the audio file to analyze'):
        start_time, end_time = 0, duration

        values = st.slider(
            'Select a duration (second) of the audio file',
            start_time, end_time, (start_time, end_time))

        # Convert time to samples
        start_sample = int(values[0] * sr)
        end_sample = int(values[1] * sr)

        # Extract the part of the audio file
        y = y[start_sample:end_sample]
        if is_stereo:
            y_stereo = y_stereo[:, start_sample:end_sample]

        st.audio(y, format='audio/ogg', sample_rate=sr)

    # print(f'y_stereo.shape {y_stereo.shape if is_stereo else y_stereo} y.shape {y.shape}, sr {sr}')

    st.divider()
    st.subheader("Step 2: Choose a processing method from left side bar")

    if not process_name:
        st.stop()

    if process_name == audio_process_lst[0]:
        st.write('***Visualize an STFT power spectrum***')

        fig, ax = plt.subplots(nrows=2, ncols=1, sharex=True)
        D = librosa.amplitude_to_db(np.abs(librosa.stft(y)), ref=np.max)
        img = librosa.display.specshow(D, y_axis='linear', x_axis='time',
                                       sr=sr, ax=ax[0])
        ax[0].set(title='Linear-frequency power spectrogram')
        ax[0].label_outer()

        librosa.display.specshow(D, y_axis='log', sr=sr,
                                 x_axis='time', ax=ax[1])
        ax[1].set(title='Log-frequency power spectrogram')
        ax[1].label_outer()
        fig.colorbar(img, ax=ax, format="%+2.f dB")
        st.pyplot(fig)

        st.write('***Plot a monophonic waveform with an envelope view***')

        fig2, ax = plt.subplots(nrows=(3 if is_stereo else 2), sharex=True)
        fig2.tight_layout()

        y_harm, y_perc = librosa.effects.hpss(y)
        librosa.display.waveshow(y_harm, sr=sr, alpha=0.5, ax=ax[0], label='Harmonic', color="blue")
        librosa.display.waveshow(y_perc, sr=sr, color='r', alpha=0.5, ax=ax[0], label='Percussive')
        ax[0].set(title='Multiple waveforms')
        ax[0].label_outer()

        librosa.display.waveshow(y, sr=sr, ax=ax[1], color="blue")
        ax[1].set(title='Envelope view, mono')
        ax[1].label_outer()

        if is_stereo:
            librosa.display.waveshow(y_stereo, sr=sr, ax=ax[2], color="blue")
            ax[2].set(title='Envelope view, stereo')
            ax[2].legend()
        else:
            ax[1].legend()

        st.pyplot(fig2)

        st.write('***Plotting a transposed wave along with a self-similarity matrix***')

        fig3, ax = plt.subplot_mosaic("hSSS;hSSS;hSSS;.vvv")
        fig3.tight_layout()
        chroma = librosa.feature.chroma_cqt(y=y, sr=sr)
        sim = librosa.segment.recurrence_matrix(chroma, mode='affinity')
        librosa.display.specshow(sim, ax=ax['S'], sr=sr,
                                 x_axis='time', y_axis='time',
                                 auto_aspect=False)
        ax['S'].label_outer()
        ax['S'].sharex(ax['v'])
        ax['S'].sharey(ax['h'])
        ax['S'].set(title='Self-similarity')
        librosa.display.waveshow(y, ax=ax['v'], color="blue")
        ax['v'].label_outer()
        ax['v'].set(title='transpose=False')
        librosa.display.waveshow(y, ax=ax['h'], transpose=True, color="blue")
        ax['h'].label_outer()
        ax['h'].set(title='transpose=True')
        st.pyplot(fig3)

    elif process_name == audio_process_lst[1]:

        st.write('***Compute a chromagram from a power spectrogram***')

        S = np.abs(librosa.stft(y, n_fft=4096)) ** 2
        chroma = librosa.feature.chroma_stft(S=S, sr=sr)

        fig1_0, ax = plt.subplots(nrows=2, sharex=True)
        img = librosa.display.specshow(librosa.amplitude_to_db(S, ref=np.max),
                                       y_axis='log', x_axis='time', ax=ax[0])
        fig1_0.colorbar(img, ax=[ax[0]])
        ax[0].label_outer()
        img = librosa.display.specshow(chroma, y_axis='chroma', x_axis='time', ax=ax[1])
        fig1_0.colorbar(img, ax=[ax[1]])
        st.pyplot(fig1_0)

    elif process_name == audio_process_lst[2]:
        st.write('***Decompose a magnitude spectrogram into 16 components with NMF***')

        S = np.abs(librosa.stft(y))
        comps, acts = librosa.decompose.decompose(S, n_components=16,
                                                  sort=True)

        layout = [list(".AAAA"), list("BCCCC"), list(".DDDD")]
        fig2_1, ax = plt.subplot_mosaic(layout, constrained_layout=True)
        librosa.display.specshow(librosa.amplitude_to_db(S, ref=np.max),
                                 y_axis='log', x_axis='time', ax=ax['A'])
        ax['A'].set(title='Input spectrogram')
        ax['A'].label_outer()
        librosa.display.specshow(librosa.amplitude_to_db(comps,
                                                         ref=np.max),
                                 y_axis='log', ax=ax['B'])
        ax['B'].set(title='Components')
        ax['B'].label_outer()
        ax['B'].sharey(ax['A'])
        librosa.display.specshow(acts, x_axis='time', ax=ax['C'], cmap='gray_r')
        ax['C'].set(ylabel='Components', title='Activations')
        ax['C'].sharex(ax['A'])
        ax['C'].label_outer()
        S_approx = comps.dot(acts)
        img = librosa.display.specshow(librosa.amplitude_to_db(S_approx,
                                                               ref=np.max),
                                       y_axis='log', x_axis='time', ax=ax['D'])
        ax['D'].set(title='Reconstructed spectrogram')
        ax['D'].sharex(ax['A'])
        ax['D'].sharey(ax['A'])
        ax['D'].label_outer()
        fig2_1.colorbar(img, ax=list(ax.values()), format="%+2.f dB")
        st.pyplot(fig2_1)

    elif process_name == audio_process_lst[3]:
        st.write('***Cluster by chroma similarity, break into 20 segments***')

        chroma = librosa.feature.chroma_cqt(y=y, sr=sr)
        bounds = librosa.segment.agglomerative(chroma, 20)
        bound_times = librosa.frames_to_time(bounds, sr=sr)

        fig3_0, ax = plt.subplots()
        trans = mpt.blended_transform_factory(
            ax.transData, ax.transAxes)
        librosa.display.specshow(chroma, y_axis='chroma', x_axis='time', ax=ax)
        ax.vlines(bound_times, 0, 1, color='linen', linestyle='--',
                  linewidth=2, alpha=0.9, label='Segment boundaries',
                  transform=trans)
        ax.legend()
        ax.set(title='Power spectrogram')
        st.pyplot(fig3_0)


if __name__ == "__main__":
    main()
