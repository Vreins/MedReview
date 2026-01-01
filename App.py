import streamlit as st
from streamlit_option_menu import option_menu
from PIL import Image
# from streamlit_searchbox import st_searchbox
import pandas as pd
import matplotlib.pyplot as plt
import csv
from SideEffect import describe_age
from datetime import datetime, time
import random
from Sentiment import get_sentiment, get_side_effects
import time
import os

data=pd.read_csv("webmd.csv")
data['Date'] = pd.to_datetime(data['Date'], format='%d/%m/%Y', errors='coerce')


image = Image.open('images/Title.png')
image = image.resize((140, 40))
st.image(image)

selected = option_menu(
    menu_title = None,
    options = ["Home", "Sentiment Identifier", "Side Effect Identifier"],
    icons = ["house-fill", "sign-intersection", "x-square"],
    default_index=0,
    orientation="horizontal"
)

# sid = SentimentIntensityAnalyzer()
#     sentiment_dict=sid.polarity_scores(text)
#     return sentiment_dict['compound']

if selected == "Home":
    col1, col2 = st.columns(2)

    with col1:
        st.title(':green[Find the Medication That Suits You Best]')
        st.caption(
            """
            <b>
            1. Different medications affect people in different ways.<br><br>
            2. Explore real patient experiences to understand benefits, side effects, and effectiveness.<br><br>
            3. Use our review and side-effect identifier features to learn from people within your age group.<br><br>
            4. Compare medications and make more informed decisions about your treatment options.
            </b>
            """,
            unsafe_allow_html=True
        )

    with col2:
        image = Image.open('images/Frame_4.jpg')
        image = image.resize((600, 750))   # (width, height) in pixels
        st.image(image)
elif selected == "Sentiment Identifier":
    
    st.title(':green[Sentiment Identifier]')
    st.caption(
    "<b>Use this feature to compare :green[drug reviews by sentiment].<br>"
    "See real user experiences and understand how others responded to different medications.<br><br>"
    "This can help you make more informed treatment decisions.</b>",
    unsafe_allow_html=True
    )

    # data[data["Drug"]=="alprazolam er"]["Description"][0]

    # This function filters results based on user query
    # def search_drugs(searchterm: str):
    #     """Return filtered results based on user input (only after 2+ chars)."""
    #     # Wait until at least 2 characters are typed
    #     if not searchterm: 
    #     # or len(searchterm) < 2:
    #         return drugs
        
    #     results = [drug for drug in drugs if searchterm.lower() in drug.lower()]
    #     return results or ["No matches found"]
    
    def add_review_section(drug_name,Condition,Description, Sides):
        st.write("")

        with st.expander(f"➕ Add Your Own Review"):
            st.write(f"This review will be added for **{drug_name}**.")
            add_review_1,add_review_2 = st.columns(2)
            with add_review_1:
                age_input = st.selectbox(
                    "Your age group:",
                    ["13-18", "19-24", "25-34", "35-44", "45-54", "55-64", "75 or over"]
                    )
            with add_review_2:
                sex_input = st.radio("Sex:", ["Female", "Male","Other"], horizontal=True)
            
            review_text = st.text_area("Write your detailed review, including your experience and thoughts and side effects if any:")
            side_effects = st.text_area("Mention any side effects experienced (optional):")
            submitted = st.button("Submit Review")
            
            date_input = datetime.now().strftime("%d/%m/%Y")
            
            # submitted = st.button("Submit Review")

            if submitted:
                if review_text.strip() == '':
                    st.toast('You cant submit an empty review', icon='❌')
                elif review_text.isdigit():
                    st.toast('You cant submit a number as a review', icon='❌')
                elif len(review_text.split()) < 10:
                    st.toast('Insufficient words', icon='❌')
                else:
                    st.toast('Reached spinner', icon='❌')
                    time.sleep(10)
                    # Process sentiment
                    try:
                        st.toast('Reached get_sentiment', icon='❌')
                        sentiments, side_1 = get_sentiment(review_text)
                        st.toast('Passed get_sentiment', icon='❌')
                    except Exception as e:
                        st.toast('Reached get_sentiment except', icon='❌')
                        sentiments = "Neutral"
                        side_1 = ""
                    
                    st.toast('Just before side effects', icon='❌')
                    # Process side effects
                    side_2 = ""
                    if side_effects.strip() != '':
                        st.toast('Reached get_side_effects', icon='❌')
                        try:
                            side_2 = get_side_effects(side_effects)
                        except Exception as e:
                            st.toast('Reached get_side_effects except', icon='❌')
                            side_2 = ""

                    # Combine side effects
                    Sides_combined = f"{Sides}, {side_1}, {side_2}".strip(", ")

                    # Build new row
                    date_input = datetime.now().strftime("%d/%m/%Y")
                    new_row = [
                        "",                                   # Index (blank)
                        age_input,                            # Age
                        Condition,                            # Condition
                        date_input,                           # Date
                        drug_name,                            # Drug
                        Description,                          # Description
                        "",                                   # DrugId
                        "",                                   # EaseofUse
                        "",                                   # Effectiveness
                        review_text,                          # Reviews
                        "",                                   # Satisfaction
                        sex_input,                            # Sex
                        Sides_combined,                       # Sides
                        "",                                   # UsefulCount
                        "",                                   # Score
                        sentiments                            # Sentiment
                    ]

                    # Append to CSV
                    with open("webmd.csv", "a", newline="", encoding="utf-8") as csvfile:
                        writer = csv.writer(csvfile)
                        writer.writerow(new_row)

                    # Clear textboxes by rerunning after delay
                    st.success("Your review has been added!")
                    st.experimental_rerun()
    def sentiment_widgets(choice):
        st.markdown(
            f"""
            <div style='text-align: center;'>
                <h2 style='color: green; margin-bottom: 0;'>{choice.title()}</h2>
                <h3 style='margin-top: 5px;'>Drug Description and Sentiment Overview</h3>
            </div>
            """,
            unsafe_allow_html=True
        )

        # -------------------------
        # 🔹 FILTERS: Gender + Age
        # -------------------------
        filter_col1, filter_col2 = st.columns(2)

        with filter_col1:
            gender_selected = st.radio(
                "Select Gender:",
                ["All", "Female", "Male"],
                horizontal=True
            )

        with filter_col2:
            age_groups = ["All", "13-18", "19-24", "25-34", "35-44", "45-54", "55-64","75 or over"]
            age_selected = st.selectbox("Select Age Group:", age_groups)

        # -------------------------
        # 🔹 APPLY FILTERS TO DATA
        # -------------------------
        filtered_data = data[data["Drug"] == choice]

        if gender_selected != "All":
            filtered_data = filtered_data[filtered_data["Sex"] == gender_selected]

        if age_selected != "All":
            # Expecting Age column numeric
            filtered_data = filtered_data[filtered_data["Age"]== age_selected]
            
        if filtered_data.empty:
            st.warning("No data available for this drug with the selected filters.")
            return

        # -------------------------
        # 🔹 DESCRIPTION SECTION
        # -------------------------
        about_col1, about_col2 = st.columns(2)

        desc = filtered_data["Description"].iloc[0]

        with about_col1:
            st.caption(desc)

        # -------------------------
        # 🔹 PIE CHART BASED ON FILTERED DATA
        # -------------------------
        with about_col2:
            sentiment_counts = filtered_data['Sentiment'].value_counts()

            fig, ax = plt.subplots()
            colors = ['#66b3ff', '#99ff99', '#ff9999']
            ax.pie(
                sentiment_counts.values,
                labels=sentiment_counts.index,
                autopct='%1.1f%%',
                colors=colors[:len(sentiment_counts)],
                startangle=90
            )
            ax.axis('equal')
            st.pyplot(fig)

        # -------------------------
        # 🔹 REVIEWS FILTERED
        # -------------------------
        def get_filtered_reviews(sentiment):
            temp = filtered_data[filtered_data['Sentiment'] == sentiment].copy()
            temp = temp[temp['Date'].notna()].copy()
            temp = temp.sort_values(by='Date', ascending=False)
            temp['day'] = temp['Date'].dt.day.astype('Int64')
            temp['month'] = temp['Date'].dt.month.astype('Int64')
            temp['year'] = temp['Date'].dt.year.astype('Int64')
            return list(temp[['Reviews', 'day', 'month', 'year']].itertuples(index=False, name=None))[:3]

        pos_reviews = get_filtered_reviews("Positive")
        neu_reviews = get_filtered_reviews("Neutral")
        neg_reviews = get_filtered_reviews("Negative")

        st.markdown(
            f"""
            <div style='text-align: center;'>
                <h3 style='margin-top: 5px;'>Drug Reviews by Users</h3>
            </div>
            """,
            unsafe_allow_html=True
        )

        tab1, tab2, tab3 = st.tabs(["😃:green[Positive]", "😐Neutral", "😫:red[Negative]"])

        def show_reviews(reviews):
            for review, day, month, year in reviews:
                if not review or str(review).lower() == "nan":
                    review = ""   # prevents "None" from printing

                st.caption(
                    unsafe_allow_html=True,
                    body=review + f"\n\n<b>{day}/{month}/{year}</b>"
                )
        with tab1:
            show_reviews(pos_reviews) if pos_reviews else st.info("No positive reviews found.")

        with tab2:
            show_reviews(neu_reviews) if neu_reviews else st.info("No neutral reviews found.")

        with tab3:
            show_reviews(neg_reviews) if neg_reviews else st.info("No negative reviews found.")
        
        add_review_section(choice,filtered_data["Condition"].iloc[0],filtered_data["Description"].iloc[0], filtered_data["Sides"].iloc[0])

    view_option = st.radio(
    "Select drug by condition or drug:",
    [" Select drug by condition", " Select drug by name"],
    horizontal=True
    )
    if view_option == " Select drug by condition":
        con_1, con_2 = st.columns(2)

        with con_1:
            conditions = data['Condition'].unique().tolist()
            conditions.insert(0, "<Choose One>")  # 👈 Add placeholder at the top

            condition_selected = st.selectbox(
                "Select a condition:",
                options=conditions,
                index=0  # 👈 Default selection
            )

        with con_2:
            if condition_selected and condition_selected != "<Choose One>":
                filtered_data = data[data['Condition'] == condition_selected]
                drug_options = filtered_data['Drug'].unique().tolist()
                drug_options.insert(0, "<Choose One>")  # 👈 Add placeholder here too

                drug_selected = st.selectbox(
                    "Select a drug:",
                    options=drug_options,
                    index=0
                )
        try:
            if drug_selected != "<Choose One>":
                sentiment_widgets(drug_selected)
        except Exception as e:
            pass
    elif view_option == " Select drug by name":
        # # Searchbox replaces selectbox
        # option = st_searchbox(
        # search_function=search_drugs,
        # key="drug_search",
        # placeholder="Start typing to search for a contraceptive...",
        # label="Choose a contraceptive:"
        # )

        # if option and option != "No matches found":
        #     st.success(f"You selected **{option}**")
        drug_options = data['Drug'].unique().tolist()
        drug_options.insert(0, "<Choose One>")  # 👈 Add placeholder here too
        drug_selected = st.selectbox(
                    "Select a drug:",
                    options=drug_options,
                    index=0
                )
        try:
            if drug_selected != "<Choose One>":
                sentiment_widgets(drug_selected)
        except Exception as e:
            pass
elif selected == "Side Effect Identifier":
    def add_side_effect_section(drug_name):
        st.write("")

        with st.expander("➕ Add Side Effect Review, if any"):
            st.header("Personal Information")
            add_effect_1, add_effect_2, add_effect_3 = st.columns(3)
            with add_effect_1:
                age_input = st.number_input("Your age:", min_value=13, max_value=75, step=1)
            with add_effect_2:
                sex_input = st.radio("Sex:", ["Female", "Male", "Other"], horizontal=True)
            with add_effect_3:
                weight_input = st.number_input("Your weight (kg):", min_value=30, max_value=200, step=1)

            st.header("Suspected Side Effect Review")
            reaction_1, reaction_2 = st.columns(2)
            with reaction_1:
                event_start = st.date_input("Reaction start date:")
            with reaction_2:
                event_end = st.date_input("Reaction end date:")

            reaction_text = st.text_area("Describe Event/Reaction (required):", key="reaction_text")
            relevant_info = st.text_area("Relevant medical history (optional):")

            reaction_severity = st.radio("Seriousness:", ["Non-Serious", "Serious"], horizontal=True)
            
            hospitalization = []
            if reaction_severity == "Serious":
                hospitalization = st.multiselect("Seriousness Type:", 
                                                ["Death", "Hospitalization", "Life-threatening", 
                                                "Congenital Anomaly", "Disability"])

            Outcome = st.radio("Outcome:", ["Recovered", "Not Recovered", "Recovering", "Unknown", "Fatal"], horizontal=True)

            st.header("Suspected Drug Information")
            st.write(f"Drug Name: **{drug_name}**")

            new_drug = st.radio("Add a new drug?", ["No", "Yes"], horizontal=True)
            if new_drug == "Yes":
                drug_name = st.text_input("Enter Drug Name:")
                drug_dosage = st.number_input("Drug Dosage (mg/day):", min_value=0)
                expiry_date = st.date_input("Drug Expiry Date:")
                date_started = st.date_input("Start Date:")
                date_stopped = st.date_input("Stop Date:")
            else:
                drug_dosage = ""
                expiry_date = ""
                date_started = ""
                date_stopped = ""

            date_input = datetime.now().strftime("%d/%m/%Y")

            st.subheader("Concomitant medications (Optional)")
            con_comitant_1, con_comitant_2, con_comitant_3, con_comitant_4 = st.columns(4)

            with con_comitant_1:
                concomitant_medications_1 = st.text_input("Medication 1:", key="med1")
                concomitant_medications_2 = st.text_input("Medication 2:", key="med2")
                concomitant_medications_3 = st.text_input("Medication 3:", key="med3")

            with con_comitant_2:
                concomitant_dose_1 = st.number_input("Dose 1 (mg):", key="dose1")
                concomitant_dose_2 = st.number_input("Dose 2 (mg):", key="dose2")
                concomitant_dose_3 = st.number_input("Dose 3 (mg):", key="dose3")

            with con_comitant_3:
                concomitant_start_1 = st.date_input("Start 1:", key="start1")
                concomitant_start_2 = st.date_input("Start 2:", key="start2")
                concomitant_start_3 = st.date_input("Start 3:", key="start3")

            with con_comitant_4:
                concomitant_stop_1 = st.date_input("Stop 1:", key="stop1")
                concomitant_stop_2 = st.date_input("Stop 2:", key="stop2")
                concomitant_stop_3 = st.date_input("Stop 3:", key="stop3")

            submitted = st.button("Submit Review")

            if submitted:

                # VALIDATION
                if reaction_text.strip() == "":
                    st.error("Reaction description cannot be empty!")
                    return

                # CSV FILE NAME
                filename = "side_effect_reports.csv"

                # CREATE FILE IF NOT EXISTS
                file_missing = not os.path.exists(filename)

                # Build row
                row = [
                    date_input,
                    drug_name,
                    drug_dosage,
                    expiry_date,
                    date_started,
                    date_stopped,
                    age_input,
                    sex_input,
                    weight_input,
                    reaction_text,
                    relevant_info,
                    str(event_start),
                    str(event_end),
                    reaction_severity,
                    ", ".join(hospitalization) if hospitalization else "",
                    Outcome,
                    # Concomitant meds
                    concomitant_medications_1, concomitant_dose_1, str(concomitant_start_1), str(concomitant_stop_1),
                    concomitant_medications_2, concomitant_dose_2, str(concomitant_start_2), str(concomitant_stop_2),
                    concomitant_medications_3, concomitant_dose_3, str(concomitant_start_3), str(concomitant_stop_3)
                ]

                # Write row to CSV
                with open(filename, "a", newline="", encoding="utf-8") as f:
                    writer = csv.writer(f)

                    # Write header when file is new
                    if file_missing:
                        writer.writerow([
                            "Date Submitted", "Drug Name","Drug Dosage", 
                            "Expiry Date", "Date Started",
                             "Date Stopped", "Age", "Sex", "Weight",
                            "Reaction Description", "Relevant History",
                            "Event Start", "Event End", "Severity",
                            "Seriousness Details", "Outcome",
                            "Med1", "Dose1", "Start1", "Stop1",
                            "Med2", "Dose2", "Start2", "Stop2",
                            "Med3", "Dose3", "Start3", "Stop3"
                        ])

                    writer.writerow(row)

                st.success("Your side effect review has been submitted successfully!")
                st.balloons()

    

    st.title(':green[Side Effect Identifier]')
    st.caption(unsafe_allow_html=True, body="<b>This feature helps you explore :green[reported side effects] experienced by people within your age group.\n\nUse it to understand how others responded to different medications and make more informed decisions about your treatment.</b>")
    
    view_option = st.radio(
        "Select drug by condition or drug:",
        [" Select drug by condition", " Select drug by name"],
        horizontal=True
    )

    if view_option == " Select drug by condition":
        con_1, con_2 = st.columns(2)
        with con_1:
            conditions = data['Condition'].unique().tolist()
            conditions.insert(0, "<Choose One>")
            condition_selected = st.selectbox("Select a condition:", options=conditions, index=0)

        with con_2:
            drug_selected = "<Choose One>"  # default value
            if condition_selected != "<Choose One>":
                filtered_data = data[data['Condition'] == condition_selected]
                drug_options = filtered_data['Drug'].unique().tolist()
                drug_options.insert(0, "<Choose One>")
                drug_selected = st.selectbox("Select a drug:", options=drug_options, index=0)

        cond_new_con_1, cond_new_con_2= st.columns(2)
        with cond_new_con_1:
            number = st.number_input(label='How old are you?', min_value=18, max_value=64, value=18)
            st.write(str(number)+" <b>Years Old</b>", unsafe_allow_html=True)
        with cond_new_con_2:
            gender = st.radio("Select your gender:", ["Female", "Male","Other"], horizontal=True)

        valid_selection = condition_selected != "<Choose One>" and drug_selected != "<Choose One>"

        if not valid_selection:
            st.warning("Please select both a condition and a drug before continuing.")

        if st.button("Identify", disabled=not valid_selection):
            response = describe_age(age=number, gender=gender, drug=drug_selected, condition=condition_selected)

            top_side_effects = ", ".join(f"'{item}'" for item in response["side_effects"])
            st.caption(unsafe_allow_html=True,
                body=f"Based on your age group {response['age_group']}, the most complained side effects are <b>{top_side_effects}</b>.\n\nBelow are the top 5 most useful drug reviews from people with your age group:\n"
            )

            for i in range(len(response["sorted_reviews"]["Reviews"])):
                st.caption(
                    unsafe_allow_html=True,
                    body=(
                        f"{i+1}. {response['sorted_reviews']['Reviews'][i]} "
                        f"<br><b><i>Drug:</i></b> :green[{response['sorted_reviews']['Drugs'][i]}] "
                        f"<br><b><i>Condition:</i></b> :blue[{response['sorted_reviews']['Conditions'][i]}]"
                    )
                )
        add_side_effect_section(drug_selected)
    elif view_option == " Select drug by name":
        drug_options = data['Drug'].unique().tolist()
        drug_options.insert(0, "<Choose One>")
        drug_selected = st.selectbox("Select a drug:", options=drug_options, index=0)

        new_con_1, new_con_2 = st.columns(2)
        with new_con_1:
            number = st.number_input(label='How old are you?', min_value=18, max_value=64, value=18)
            st.write(str(number)+" <b>Years Old</b>", unsafe_allow_html=True)
        with new_con_2:
            gender = st.radio("Select your gender:", ["Female", "Male","Other"], horizontal=True)

        valid_selection = drug_selected != "<Choose One>"

        if not valid_selection:
            st.warning("Please select a drug before continuing.")

        if st.button("Identify", disabled=not valid_selection):
            response = describe_age(age=number, gender=gender, drug=drug_selected, condition=None)

            top_side_effects = ", ".join(f"'{item}'" for item in response["side_effects"])
            st.caption(unsafe_allow_html=True,
                body=f"Based on your age group {response['age_group']}, the most complained side effects are <b>{top_side_effects}</b>.\n\nBelow are the top 5 most useful contraceptive reviews from people with your age group:\n"
            )

            for i in range(len(response["sorted_reviews"]["Reviews"])):
                st.caption(
                    unsafe_allow_html=True,
                    body=(
                        f"{i+1}. {response['sorted_reviews']['Reviews'][i]} "
                        f"<br><b><i>Drug:</i></b> :green[{response['sorted_reviews']['Drugs'][i]}] "
                        f"<br><b><i>Condition:</i></b> :blue[{response['sorted_reviews']['Conditions'][i]}]"
                    )
                )
        add_side_effect_section(drug_selected)