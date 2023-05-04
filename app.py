import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
from scipy.stats import ttest_ind

# set page to wide
st.set_page_config(layout="wide")

st.title("Significance Tester")
st.markdown("**This is a simple web app to test the significance of a difference between two groups.**")

# generate data
# mean imput box
with st.form(key='my_form'):
    st.markdown("### Step 1: Generate Distributions")
    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown("### A Group")
        # mean input box
        mean_input1 = st.number_input("Mean", value=100.0, step=0.1, key='mean_input1')
        # standard deviation input box
        std_input1 = st.number_input("Standard Deviation", value=60.0, step=0.1, key='std_input1')
        # sample size input box
        sample_size_input1 = st.number_input("Sample Size", value=200, step=1, key='sample_size_input1')
    with col2:
        st.markdown("### B Group")
        # mean input box
        mean_input2 = st.number_input("Mean", value=110.0, step=0.1, key='mean_input2')
        # standard deviation input box
        std_input2 = st.number_input("Standard Deviation", value=50.0, step=0.1, key='std_input2')
        # sample size input box
        sample_size_input2 = st.number_input("Sample Size", value=200, step=1, key='sample_size_input2')

    st.markdown("#### Some options")
    col1, col2, col3, col4, col5, col6 = st.columns([1, 1, 1, 1, 1, 1])
    with col1:
        # checkbox for show data
        show_dist = st.checkbox("Show Separete Distributions", value=False, key='show_dist')
    with col2:
        # checkbox for show data
        show_data = st.checkbox("Show Data Table", value=False, key='show_data')
    with col3:
        # checkbox for describing the data
        describe_data = st.checkbox("Describe Data", value=False, key='describe_data')

    st.markdown("### Step 2: Draw samples from the distributions (with replacement)")
    # sample size input box
    sample_size_input = st.number_input("Sample Size (Draw this many samples from A group and B group)", value=100, step=1, key='sample_size_input')
    # times to repeat input box
    times_to_repeat_input = st.number_input("Times to Repeat the Drawing", value=10000, step=1,
                                            key='times_to_repeat_input')
    # submit button
    generate_distibrutions_button = st.form_submit_button(label='Genarate Distributions')

st.markdown("Since it is a random process, the distributions will change every time you click the button.")
st.markdown("This time you got the followings")
# generate data
if generate_distibrutions_button:
    # generate data
    group1 = np.random.normal(mean_input1, std_input1, sample_size_input1)
    group2 = np.random.normal(mean_input2, std_input2, sample_size_input2)

    # create dataframe
    df1 = pd.DataFrame(group1, columns=['value'])
    df1['group'] = 'A'
    df2 = pd.DataFrame(group2, columns=['value'])
    df2['group'] = 'B'

    df_all = pd.concat([df1, df2], axis=0, ignore_index=True)
    if show_data:
        st.dataframe(df_all)

    col1, col2 = st.columns([1, 1])
    if show_dist:
        with col1:
            st.markdown("### Group A")
            if describe_data:
                st.dataframe(df1.describe())
            # plot histogram of group 1 with color red
            fig1 = px.histogram(df1, x='value', marginal='box', color='group', barmode='overlay',
                                color_discrete_sequence=['red'])
            st.plotly_chart(fig1, use_container_width=True)
        with col2:
            st.markdown("### Group B")
            if describe_data:
                st.dataframe(df2.describe())
            # plot histogram of group 2 with color blue
            fig2 = px.histogram(df2, x='value', marginal='box', color='group', barmode='overlay',
                                color_discrete_sequence=['blue'])
            # add line to the mean of group 2
            fig2.add_vline(x=mean_input2, line_width=3, line_dash="dash", line_color="blue", annotation_text="Mean")
            st.plotly_chart(fig2, use_container_width=True)

    st.markdown("### Step 1: Distributions")
    st.markdown("Distribution of the two groups.")
    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown("**A Group** was generated using: mean = " + str(mean_input1) + ", standard deviation = " + str(
            std_input1) + ", and sample size = " + str(sample_size_input1) + ".")
    with col2:
        st.markdown("**B Group** was generated using: mean = " + str(mean_input2) + ", standard deviation = " + str(
            std_input2) + ", and sample size = " + str(sample_size_input2) + ".")

    # plot both together where color is determined by the group (group1 is red, group2 is blue)
    fig3 = px.histogram(df_all, x='value', marginal='box', color='group', barmode='overlay',
                        color_discrete_sequence=['tomato', 'blue'])
    min_valeu_sample = df_all['value'].min()
    max_valeu_sample = df_all['value'].max()
    fig3.update_xaxes(range=[min_valeu_sample, max_valeu_sample])
    st.plotly_chart(fig3, use_container_width=True)

    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown("The **mean** of A group is: " + str(df1['value'].mean()))
        st.markdown("The **sd** of A group is: " + str(df1['value'].std()))
        st.markdown("The **sample size** of A group is: " + str(df2['value'].count()))
    with col2:
        st.markdown("The **mean** of B group is: " + str(df2['value'].mean()))
        st.markdown("The **sd** of B group is: " + str(df2['value'].std()))
        st.markdown("The **sample size** of B group is: " + str(df2['value'].count()))

    st.markdown("#### The classical t test")
    #calculate p values with t test for the two groups
    t_test, p_value = ttest_ind(df1['value'], df2['value'])
    # display p value
    st.markdown("The t test for the two groups is: " + str(t_test))
    st.markdown("The p value for the two groups is: " + str(p_value))

    if p_value < 0.05:
        st.markdown("**The two groups are significantly different.**")
    else:
        st.markdown("**The two groups are NOT significantly different.**")

    with st.spinner('Wait for it...'):
        # create long format of the data
        #sample1 = pd.concat([df1.sample(sample_size_input, replace=True).assign(sample=i, group='A') for i in range(times_to_repeat_input)], ignore_index=True)
        #sample2 = pd.concat([df2.sample(sample_size_input, replace=True).assign(sample=i, group='B') for i in range(times_to_repeat_input)], ignore_index=True)
        # create sample1 and sample2 in one go
        samples = [pd.concat(
            [df.sample(sample_size_input, replace=True).assign(sample=i, group=group) for i in
             range(times_to_repeat_input)], ignore_index=True) for df, group in
                   [(df1, 'A'), (df2, 'B')]]

        sample1, sample2 = samples
        sample_all_long = pd.concat([sample1, sample2], axis=0, ignore_index=True)

        # calculate the mean of each sample using group by
        sample_statistics = sample_all_long.groupby(['group', 'sample']).agg(
            count=('value', 'count'),
            mean=('value', 'mean'),
            median=('value', 'median'),
            std=('value', 'std')
        ).reset_index()



        st.markdown("### Step 2: The sample mean distributions")
        st.markdown('The sample mean distributions are the distributions of the means of the samples.')
        st.markdown('We get this by drawing samples from the population and calculating the mean of each sample.')
        st.markdown('Currently we are drawing {} samples {} times from both of the population.'.format(sample_size_input, times_to_repeat_input))
        # plot histogram of sample means
        fig4 = px.histogram(sample_statistics, x='mean', marginal='box', color='group', barmode='overlay',
                            color_discrete_sequence=['peru', 'teal'])
        # set the x axis range
        fig4.update_xaxes(range=[min_valeu_sample, max_valeu_sample])
        st.plotly_chart(fig4, use_container_width=True)


        sample_all_wide = sample_statistics.pivot(index='sample', columns='group',
                                                  values='mean').reset_index()
        sample_all_wide['difference'] = sample_all_wide['B'] - sample_all_wide['A']
        sample_all_wide['difference_count'] = np.where(sample_all_wide['difference'] > 0, 1, 0)

        st.markdown("### Step 3: The mean difference distribution")
        st.markdown('The mean difference distribution is the distribution of the difference between the means of the samples.')
        st.markdown('We get this by subtracting the mean of each sample from the other.')
        st.markdown('Currently we are drawing {} samples {} times from both of the population.'.format(sample_size_input, times_to_repeat_input))
        # plot histogram of sample means
        fig5 = px.histogram(sample_all_wide, x='difference', marginal='box', color_discrete_sequence=['red'])
        # set the x axis range
        st.plotly_chart(fig5, use_container_width=True)

        # count how many times the difference is less than 0
        count = sample_all_wide['difference_count'].sum()
        percent = count / times_to_repeat_input
        st.markdown('The ratio that the difference between the means of the samples is less than 0 is: ' + str(percent))
        if percent > 0.95:
            st.markdown("The probability is more than 0.95, so we reject the null hypothesis.")
            st.markdown("**The two groups are significantly different.**")
        else:
            st.markdown("The probability is less than 0.05, so we fail to reject the null hypothesis.")
            st.markdown("**The two groups are NOT significantly different.**")






