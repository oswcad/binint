import streamlit as st
import pandas as pd
import numpy as np

hide_menu = """
<style>
/* #MainMenu { 
     visibility: hidden; 
} */

footer {
    visibility: visible;
}
footer:after{
    content:"By: Oswaldo Cadenas, 2022";
    display: block;
    position: relative;
    color: tomato;
}
</style>
"""
numsuper = {0: '2\u2070', 1: '2\u00b9', 2: '2\u00b2', 3: '2\u00b3', 4: '2\u2074', 5: '2\u2075',
            6: '2\u2076', 7: '2\u2077', 8: '2\u2078', 9: '2\u2079', 10: '2\u00b9\u2070',
            11: '2\u00b9\u00b9', 12: '2\u00b9\u00b2', 13: '2\u00b9\u00b3', 14: '2\u00b9\u2074',
            15: '2\u00b9\u2075'}


st.sidebar.image('LSBU_2020_BO.png', width=200)
# st.title('EEE_4_DLD: Combinational Logic')
title = '<p style="font-family:verdana; color:#ff1010; font-size: 36px;"><b>EEE_4_DLD: Integers in binary</b></p>'
st.markdown(hide_menu, unsafe_allow_html=True)
st.markdown(title, unsafe_allow_html=True)

help = st.sidebar.expander("How to use")
help.write("""

- Enter the number of bits and a decimal number

Results appear in either of three tabs of:

- Powers of 2
- Natural binary
- 2's complement

""")

def n2bin(decimal, bits):
    # This is a decimal to natural binary conversion
    # the outpus is padded with zeros to the left 
    # so it returns a string with the value of 'bits'  
    bvalue = bin(decimal)[2:]
    pad = bits - len(bvalue)
    bvaluepadded = "0"*pad + bvalue
    return bvaluepadded


st.sidebar.markdown('**Parameters**')

# inputs
no_bits = st.sidebar.number_input('Size in bits', min_value=1, max_value=13, value = 4, step=1, format='%d')

number = st.sidebar.text_input('Decimal number to be converted', placeholder="Range will be checked based on bits")

bin_integer = st.sidebar.radio(
    "Desired binary representation",
    ("Natural binary", "2's complement"))

tab1, tab2, tab3 = st.tabs(["Powers of 2", "Natural binary", "2's complement"])

with tab1:
    headers = [numsuper[i] for i in range(no_bits-1, -1, -1)]
    powers = np.array([2**i for i in range(no_bits-1, -1, -1)], dtype=np.int32)
    table = pd.DataFrame(powers.reshape(1, no_bits), columns=headers, index = ['Weights'])
    st.write(f'The base 2 is raised to the power of position, starting from position 0 at the right, like so:')
    st.dataframe(data=table)
    st.markdown(f"Position {headers[-1]} with weight 1 is referred to as **LSB** (*Least Significant Bit*)")
    st.markdown(f"Position {headers[0]} with weight {powers[0]} is referred to as **MSB** (*Most Significant Bit*)")

with tab2:
    if bin_integer == 'Natural binary':
        if number == '':
            st.sidebar.warning(f"Enter a decimal number")
            st.stop()
        else:
            value = int(number)
            lmin, lmax = 0, 2**no_bits
            if (value >= lmax) or (value < lmin):
                st.sidebar.warning(f"With {no_bits} bits decimal value must be in range [{lmin}, {lmax-1}] for natural binary")
                st.stop()
            else:
                n_binary = n2bin(value, no_bits)
                message = f'The decimal value of **{value}** in natural binary is **{n_binary}** using {no_bits} bits'
                st.markdown(message)
                explain_binary = st.checkbox("Explain")
                if explain_binary:
                    st.write(f'The base 2 is raised to the power of position, starting from position 0 at the right, like so:')
                    st.dataframe(data=table)
                    st.markdown(f"The powers of the binary representation by position for {no_bits} bits is {powers}")
                    st.markdown(f"Position {headers[-1]} with weight 1 is referred to as **LSB** (*Least Significant Bit*)")
                    st.markdown(f"Position {headers[0]} with weight {powers[0]} is referred to as **MSB** (*Most Significant Bit*)")
                    st.write(f'So, {value} is represented by bits (bottom row):')
                    new_row = [int(i) for i in list(n_binary)]
                    new_row = np.array(new_row).reshape(1, no_bits)
                    rows = np.vstack((powers.reshape(1, no_bits), new_row))
                    bintable = pd.DataFrame(rows, columns=headers, index = ['Weights', 'Bits'])
                    st.dataframe(bintable)
                    lexp = str(value) + ' = '
                    rexp = ""
                    for bit, pow in zip(list(n_binary), list(powers)):
                        if bit == '1':
                            rexp += str(pow) + "\*" + bit + ' + '
                    rexp = rexp[:-3]
                    exp = lexp + rexp
                    st.write(exp)
                    st.markdown(f"Notice this is the *dot product* of Weights and Bits")
                    more_binary = st.checkbox("Simple table")
                    if more_binary:
                        st.write('All natural binary numbers with 3 bits ...')
                        st.write('we typically give a label to each bit, as A, B, C etc.')
                        frt = '#0' + str(5) + 'b'
                        table = [list(format(i, frt)[2:]) for i in range(2**3)]
                        table_df = pd.DataFrame(np.array(table), columns=['A', 'B', 'C'])
                        st.dataframe(table_df)

with tab3:
    if bin_integer == "2's complement":
        if number == '':
            st.sidebar.warning(f"Enter a decimal number")
            st.stop()
        else:
            value = int(number)
            lmin, lmax = -2**(no_bits-1), 2**(no_bits-1)-1
            if (value >= lmax) or (value < lmin):
                st.sidebar.warning(f"With {no_bits} bits decimal value must be in range [{lmin}, {lmax-1}] for 2's complement")
                st.stop()
            else:
                if value >= 0:
                    n2_binary = n2bin(value, no_bits)
                if value < 0:
                    newvalue = 2**no_bits + value
                    n2_binary = n2bin(newvalue, no_bits)
                message2 = f"The decimal value of **{value}** in two's complement form is **{n2_binary}** using {no_bits} bits"
                st.markdown(message2)
                explain_complement = st.checkbox("Explain")
                if explain_complement:
                    if value >= 0:
                        st.markdown(f"In 2's complement form the *maximum* positive value for *p* bits is:")
                        st.latex("2^{p-1}-1") 
                        st.write(f"that is {numsuper[no_bits-1]}-1 = {lmax} with {no_bits} bits")
                        st.write(f"\nAs the integer value is positive:")
                        st.write(f"- Write the value of {value} in natural binary")
                        st.write(f"- Make sure that {value} <= {lmax} (max with {no_bits} bits)")
                        st.write("Note that the MSB is 0 in this case")
                    if value < 0:
                        st.markdown(f"In 2's complement form the *mimimum* negative value for *p* bits is:")
                        st.latex("-2^{p-1}") 
                        st.write(f"that is -{numsuper[no_bits-1]} = {lmin} with {no_bits} bits")
                        st.write(f"- Make sure that {value} >= {lmin} (min with {no_bits} bits)")
                        st.write(f"For a decimal value *x*, with *p* bits the following property holds:")
                        st.latex("2^{p} = x + c2[x]") 
                        st.write(f"where C2[x] denotes the two's complement of x")
                        lpow = numsuper[no_bits]
                        c2n = 2**no_bits - (-value)
                        st.write(f"In summary, c2[{-value}] = {lpow} - {-value} = {2**no_bits} - {-value} = {c2n}")
                        st.markdown(f"- Then,  the two's complement of {value} is the same bit pattern as the natural binary of {c2n}; that is **{n2_binary}** ")
                        st.write(f"- Note that the MSB of {n2_binary} is 1 in this case")
                        more_complement = st.checkbox("Simpler please ...")
                        if more_complement:
                            st.write('Perhaps, simpler to undertand this way. For instance with 3 bits:')
                            st.write(f'- Build the table of all 8 numbers ({numsuper[3]}) in natural binary')
                            st.write(f'- Starting from zero, and up to half the table are positive numbers')
                            st.write(f'- From the last entry of the table, start from -1 and down to the second half are negative numbers')
                            frt = '#0' + str(5) + 'b'
                            table = [list(format(i, frt)[2:]) for i in range(2**3)]
                            table_df = pd.DataFrame(np.array(table), columns=['A', 'B', 'C'])
                            table_df["Two's complement"] = [0, 1, 2, 3, -4, -3, -2, -1]
                            st.dataframe(table_df)

