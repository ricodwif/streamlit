import streamlit as st
import numpy as np
import pandas as pd
from scipy import stats

st.title('Pengujian Distribusi')

with st.sidebar:
    tipe = st.radio('Pilih Tipe', ['Distribusi Binomial', 'Distribusi Poisson', 
                                   'Distribusi Normal', 'Distribusi T',
                                   'Distribusi F', 'Distribusi Chi-Square'])

# Function to perform distribution testing
def perform_distribution_test(data, distribution, **params):
    p_value = None
    test_result = None

    if distribution == 'Distribusi Binomial':
        # Perform Binomial distribution test
        n = params['n']
        r = params['r']
        p = params['p']
        p_value = stats.binom_test(r, n, p)
        test_result = 'Normal' if p_value > 0.05 else 'Not Normal'

    elif distribution == 'Distribusi Poisson':
        # Perform Poisson distribution test
        r = params['r']
        miu = params['miu']
        p_value = stats.kstest(data, 'poisson', args=(miu,))[1]
        test_result = 'Normal' if p_value > 0.05 else 'Not Normal'

    elif distribution == 'Distribusi Normal':
        # Perform Normal distribution test
        z = params['z']
        p_value = stats.norm.sf(z)
        test_result = 'Normal' if p_value > 0.05 else 'Not Normal'

    elif distribution == 'Distribusi T':
        # Perform T distribution test
        df = params['df']
        alfa = params['alfa']
        p_value = stats.t.sf(np.abs(data.mean() - params['z']) / (data.std() / np.sqrt(len(data))), df)
        test_result = 'Normal' if p_value > alfa else 'Not Normal'

    elif distribution == 'Distribusi F':
        # Perform F distribution test
        v1 = params['v1']
        v2 = params['v2']
        p_value = stats.f.sf(data.var() / params['z'], v1, v2)
        test_result = 'Normal' if p_value > 0.05 else 'Not Normal'

    elif distribution == 'Distribusi Chi-Square':
        # Perform Chi-Square distribution test
        df = params['df']
        alfa = params['alfa']
        p_value = stats.chisquare(data, df)
        test_result = 'Normal' if p_value > alfa else 'Not Normal'

    return p_value, test_result

# Get user input data and parameters
data = st.text_input('Masukkan data (pisahkan dengan koma)')

if tipe == 'Distribusi Binomial':
    n = st.number_input('Masukkan nilai n', min_value=0, value=1, step=1)
    r = st.number_input('Masukkan nilai r', min_value=0, value=1, step=1)
    p = st.number_input('Masukkan nilai p', min_value=0.0, max_value=1.0, value=0.5, step=0.1)
elif tipe == 'Distribusi Poisson':
    r = st.number_input('Masukkan nilai r', min_value=0, value=1, step=1)
    miu = st.number_input('Masukkan nilai miu', min_value=0.0, value=1.0, step=0.1)
elif tipe == 'Distribusi Normal':
    z = st.number_input('Masukkan nilai z', value=0.0, step=0.1)
elif tipe == 'Distribusi T':
    df = st.number_input('Masukkan nilai DF', min_value=1, value=1, step=1)
    alfa = st.number_input('Masukkan nilai alfa', min_value=0.0, max_value=1.0, value=0.05, step=0.01)
elif tipe == 'Distribusi F':
    v1 = st.number_input('Masukkan nilai v1', min_value=1, value=1, step=1)
    v2 = st.number_input('Masukkan nilai v2', min_value=1, value=1, step=1)
elif tipe == 'Distribusi Chi-Square':
    df = st.number_input('Masukkan nilai DF', min_value=1, value=1, step=1)
    alfa = st.number_input('Masukkan nilai alfa', min_value=0.0, max_value=1.0, value=0.05, step=0.01)

# Perform distribution testing when "Submit" button is clicked
if st.button('Submit'):
    try:
        data_array = np.array([float(x.strip()) for x in data.split(',')])
        p_value, test_result = perform_distribution_test(data_array, tipe, n=n, r=r, p=p, miu=miu, z=z, df=df, alfa=alfa, v1=v1, v2=v2)

        st.subheader('Hasil Pengujian')
        st.write('Nilai p-value:', p_value)
        st.write('Kesimpulan:', test_result)
    except:
        st.error('Terjadi kesalahan dalam memproses data. Pastikan data yang dimasukkan valid.')
