
def create_transient_plots(cache_main_dir):
    import matplotlib.pyplot as plt
    from basic_functions import load_json
    import warnings
    from logger import get_logger
    from basic_functions import calculate_vibration_data
    import os
    import matplotlib.image as mpimg

    logger = get_logger()
    drive = "O:"
    files_path = os.path.join("A000000", "A004371", "3_Pdoc", "Afrapportering", "files")
    files_path = os.path.normpath(drive + os.sep + files_path)
    logo_path = os.path.join(files_path,"Logo_no_background.png")

    transient_path = os.path.join(cache_main_dir, "Results","trans_dict_final.json")
    info_path = os.path.join(cache_main_dir, "API","project_sensor_dict_final.json")
    trans_dict = load_json(transient_path)
    info_dict = load_json(info_path)

    color_blue = (51/254, 129/254, 198/254)
    color_brown = (153/254, 102/254, 51/254)
    color_green = (117/254, 180/254, 73/254)

    for adresse, details in trans_dict.items():
        if "Transienter" not in details or not details["Transienter"]:
            continue

        transienter = details["Transienter"]

        reel_trans = [entry for entry in transienter if entry.get('type')==1 or entry.get('type')==3]
        
        if reel_trans == []:
            continue
        
        sensor_id = str(info_dict[adresse]["sensor_id"])
        limit = info_dict[adresse]["limit"]

        freq_V = []
        val_V = []
        freq_L = []
        val_L = []
        freq_T = []
        val_T = []

        fig, ax = plt.subplots(figsize=(15, 9))
        # Keep track of already added legend labels to avoid duplicates
        
        ax.scatter(1000,1000,s=100, color=color_blue, marker=r'$\odot$', linewidths = 0.5, facecolors=color_blue, label='Overskridelse - V')
        ax.scatter(1000, 1000, s=25, color=color_blue, marker='o', label='Hændelse - V')

        ax.scatter(1000,1000,s=100, color=color_brown, marker=r'$\odot$', linewidths = 0.5, facecolors=color_brown, label='Overskridelse - L')
        ax.scatter(1000, 1000, s=25, color=color_brown, marker='o', label='Hændelse - L')

        ax.scatter(1000,1000,s=100, color=color_green, marker=r'$\odot$', linewidths = 0.5, facecolors=color_green, label='Overskridelse - T')
        ax.scatter(1000, 1000, s=25, color=color_green, marker='o', label='Hændelse - T')
        for transient in reel_trans:
            trans_data = transient[sensor_id]['transients']
        
            for data in trans_data:
                try:
                    freq = min(100,float(data['frequency']))
                except TypeError:
                    freq = 0 
                    
                val = min(20,float(data['value']))
                per = calculate_vibration_data(freq, 3, vibration=val, percentage=None)
                if data['label'] == 'V':
                    freq_V.append(freq)
                    val_V.append(val)
                    if per > 100:
                        ax.scatter(freq, val, s=100, color=color_blue, marker=r'$\odot$', linewidths = 0.5, facecolors=color_blue)
                    else:
                        ax.scatter(freq, val, s=25, color=color_blue, marker='o')
                elif data['label'] == 'L':
                    freq_L.append(freq)
                    val_L.append(val)
                    if per > 100:
                        ax.scatter(freq, val, s=100, color=color_brown, marker=r'$\odot$', linewidths = 0.5, facecolors=color_brown)
                    else:
                        ax.scatter(freq, val, s=25, color=color_brown, marker='o')
                elif data['label'] == 'T':
                    freq_T.append(freq)
                    val_T.append(val)
                    if per > 100:
                        ax.scatter(freq, val, s=100, color=color_green, marker=r'$\odot$', linewidths = 0.5, facecolors=color_green)
                    else:
                        ax.scatter(freq, val, s=25, color=color_green, marker='o')
        
        freq = [0, 10, 50, 100]
        val_3 = [3, 3, 8, 10]
        val_5 = [5, 5, 15, 20]

        # Add lines
        if limit == 5:
            ax.plot(freq, val_5, 'r-', label='5 mm/s')
        else:
            ax.plot(freq, val_5, 'k--', label='5 mm/s')  # Dashed threshold line
            ax.plot(freq, val_3, 'r-', label='Grænseværdi')  # Solid limit line

        # Labels and title
        ax.set_xlabel('Frekvens [Hz]',fontsize=14)
        ax.set_ylabel('Peak [mm/s]',fontsize=14)
        ax.tick_params(axis='x', labelsize=12)  # Change font size for x-axis tick labels
        ax.tick_params(axis='y', labelsize=12)  # Change font size for y-axis tick labels

        ax.set_xticks(range(0, 101, 10))  # Set x-ticks every 10 units from 0 to 100
        ax.set_yticks(range(0, 21, 2))  # Set y-ticks every 10 units from 0 to 100 (adjust as necessary)
    
        ax.set_title(f'{adresse}\n{sensor_id}', fontsize=16)

        ax.set_ylim([0, 20])
        ax.set_xlim([0, 101])

        ax.legend(loc='upper left', bbox_to_anchor=(1.01, 0.95), borderaxespad=0., fontsize=8, markerscale=0.6, frameon=False,
                labelspacing=1.0, handletextpad=2.0) # Places the legend outside
        ax.grid(axis='y')

        # Add image instead of "COWI"
        img = mpimg.imread(logo_path)  # Load the image (replace with your image path)# Create a new axes that is outside the main plot
        image_axes = fig.add_axes([0.89, 0.89, 0.10, 0.10])  # [left, bottom, width, height]
        image_axes.imshow(img)
        image_axes.axis('off')  # Turn off the axes for the image

        # Customize the plot border around the main graph area
        border_color = 'black'  # Color of the border
        border_width = 2  # Thickness of the border

        # Set the border properties for each spine (left, right, top, bottom)
        for spine in ax.spines.values():
            spine.set_edgecolor(border_color)
            spine.set_linewidth(border_width)
            
        warnings.filterwarnings("ignore", category=UserWarning, message=".*tight_layout.*")
        plt.tight_layout()
        figure_path = os.path.join(cache_main_dir,"Rapport","Figurer",f"{adresse}")

        os.makedirs(figure_path, exist_ok=True)

        #plt.show()

        plt.savefig(os.path.join(figure_path,"Transienter_limit_3.jpg",))

    logger.log("Analyse af transienter er færdig", style=1, status=1)
        
def generate_transient_report(transient_data, main_text_path, text_final_path, sensor_id, Reel, Arbe, bygningstype, limit):
    import numpy as np
    from holidays import Denmark
    import holidays.countries
    from collections import defaultdict
    from datetime import timedelta, datetime, date
    from basic_functions import calculate_vibration_data
    from basic_functions import weekday_danish
    from basic_functions import month_danish
    import os

    # Define the max time window (1 hour)
    max_time_delta = timedelta(hours=2)
    
    transient_data['Transienter'] = [t for t in transient_data['Transienter'] if t.get('type') != 2]

    # Prepare to store grouped events by date
    events_by_date = defaultdict(list)
    
    # Process each transient event
    for transient in transient_data['Transienter']:
        timestamp = transient['timestamp']
        datetime_obj = datetime.fromtimestamp(timestamp)

        # Extract information from each direction and find the highest direction
        highest_direction = None
        highest_vibration = None
        highest_frequency = None

        max_percentage = 0
        above_limit_5 = False
        for id in np.unique(sensor_id):
            for direction_data in transient[id]['transients']:
                # Assuming your function is `calculate_highest_percentage` 
                vibration = float(direction_data['value'])
                try:
                    frequency = float(direction_data['frequency'])
                except TypeError:
                    frequency = 0

                #if 
                percentage = calculate_vibration_data(frequency, 3, vibration=vibration, percentage=None)
                percentage_limit_5 = calculate_vibration_data(frequency, 5, vibration=vibration, percentage=None)
                
                if percentage_limit_5 > 100 and limit != 5:
                    above_limit_5 = True

                if percentage > max_percentage:
                    max_percentage = percentage
                    highest_direction = direction_data['label']
                    highest_vibration = vibration
                    highest_frequency = frequency
            
            

        events_by_date[datetime_obj.date()].append({
            'datetime': datetime_obj,
            'max_vibration': str(highest_vibration).replace('.', ','),
            'frequency': str(highest_frequency).replace('.', ','),
            'direction': highest_direction,
            'type': transient["type"],
            'limit 5': above_limit_5
        })

        events_above_5 = defaultdict(list)

        for date_event, entries in events_by_date.items():
            for entry in entries:
                if entry.get('limit 5') == True:  # Check if the entry is above limit 5
                    events_above_5[date_event].append(entry)
    
    
    text_path = os.path.join(main_text_path, "Overskridelser_2.md")
    with open(text_path, 'r', encoding='utf-8') as file:
        text = file.read()
        
    text = text.replace("HÆNDELSE/HÆNDELSER","hændelse" if Reel + Arbe == 1 else "hændelser")
    text = text.replace("HÆNDELSEN/HÆNDELSERNE","Hændelsen" if Reel + Arbe == 1 else "Hændelserne")
    text = text.replace("TIDSPUNKT/TIDSPUNKTER","tidspunkt" if Reel + Arbe == 1 else "tidspunkter")
    text = text.replace("VIB_ELLER_NORMAL", bygningstype)
    
    text_final_file = os.path.join(text_final_path,"text_2.md")
    with open(text_final_file, 'w', encoding='utf-8') as file:
        file.write(text)
    
        # Process and format each date's events
        for date_event, events in events_by_date.items():
            
            events.sort(key=lambda x: x['datetime'])  # Sort by datetime within each day
            
            holidays_event_year = Denmark(date_event.year)
            custom_holidays = {
                date(date_event.year, 12, 24): "Christmas Eve",
                date(date_event.year, 12, 31): "New Years Eve"
            }

            holidays_event_year.update(custom_holidays)

            i = 0
            while i < len(events):
                start_event = events[i]
                start_time = start_event['datetime']

                max_vibration = start_event['max_vibration']
                frequency = start_event['frequency']
                vib_type = start_event["type"]
                
                is_weekday = start_time.weekday() < 5
                is_working_hour = 6<= start_time.hour < 17
                is_not_holiday = start_time.date() not in holidays_event_year

                outside_working_time = not (is_weekday and is_working_hour and is_not_holiday)
                # Find the end of the time window
                j = i + 1
                while j < len(events) and (events[j]['datetime'] - start_time) <= max_time_delta and vib_type == events[j]["type"]:
                    # Update max vibration, frequency, and direction if a higher value is found
                    if float(events[j]['max_vibration'].replace(",",".")) > float(max_vibration.replace(",",".")):
                        max_vibration = events[j]['max_vibration']
                        frequency = events[j]['frequency']
                    j += 1
                if j - i == 1 and vib_type == 1:
                    if outside_working_time:
                        # Single transient
                        bullet_text = (
                            f"- {weekday_danish(start_time.weekday())} den {start_time.day}. {month_danish(start_time.month)} {start_time.year} "
                            f"ca. kl. {start_time.strftime('%H:%M')}. Maksimal vibrationsniveau {max_vibration} mm/s ved {frequency} Hz. " 
                            "Det bemærkes at hændelserne er sket udenfor entreprenørens normale arbejdstid.\n"
                        )
                    else:
                        # Single transient
                        bullet_text = (
                            f"- {weekday_danish(start_time.weekday())} den {start_time.day}. {month_danish(start_time.month)} {start_time.year} "
                            f"ca. kl. {start_time.strftime('%H:%M')}. Maksimal vibrationsniveau {max_vibration} mm/s ved {frequency} Hz.\n"
                        )
                elif j - i == 1 and vib_type == 3: 
                    if outside_working_time:
                        # Single transient
                        bullet_text = (
                            f"- {weekday_danish(start_time.weekday())} den {start_time.day}. {month_danish(start_time.month)} {start_time.year} "
                            f"ca. kl. {start_time.strftime('%H:%M')}. Maksimal vibrationsniveau {max_vibration} mm/s ved {frequency} Hz.  " 
                            f"Det bemærkes at hændelserne er sket udenfor entreprenørens normale arbejdstid."
                            f"Arbejdet er formentligt udført tæt på måleren, hvorfor det vurderes at vibrationsniveauet ikke afspejler den generelle påvirkning af ejendommen. \n"
                        )
                    else:
                        bullet_text = (
                            f"- {weekday_danish(start_time.weekday())} den {start_time.day}. {month_danish(start_time.month)} {start_time.year} "
                            f"ca. kl. {start_time.strftime('%H:%M')}. Maksimal vibrationsniveau {max_vibration} mm/s ved {frequency} Hz. " 
                            f"Arbejdet er formentligt udført tæt på måleren, hvorfor det vurderes at vibrationsniveauet ikke afspejler den generelle påvirkning af ejendommen. \n"
                        )
                elif j - i != 1 and vib_type == 1:
                    # Multiple transients within time window
                    end_time = events[j - 1]['datetime']
                    weekday = weekday_danish(start_time.weekday())
                    if start_time.strftime('%H:%M') == end_time.strftime('%H:%M'):
                        time_span = f"ca. kl. {start_time.strftime('%H:%M')}"
                    else:
                        time_span = f"i perioden ca. kl. {start_time.strftime('%H:%M')} - {end_time.strftime('%H:%M')}"

                    if outside_working_time:
                        bullet_text = (
                            f"- {j - i} overskridelser {weekday.lower()} den {start_time.day}. {month_danish(start_time.month)} {start_time.year} "
                            f"{time_span}. "
                            f"Maksimalt vibrationsniveau {max_vibration} mm/s ved {frequency} Hz. "
                            f"Det bemærkes at hændelserne er sket udenfor entreprenørens normale arbejdstid. \n"
                        )
                    else:
                        bullet_text = (
                            f"- {j - i} overskridelser {weekday.lower()} den {start_time.day}. {month_danish(start_time.month)} {start_time.year} "
                            f"{time_span}. "
                            f"Maksimalt vibrationsniveau {max_vibration} mm/s ved {frequency} Hz.\n"
                        )
                elif j - i != 1 and vib_type == 3:
                    # Multiple transients within time window
                    end_time = events[j - 1]['datetime']
                    weekday = weekday_danish(start_time.weekday())

                    if start_time.strftime('%H:%M') == end_time.strftime('%H:%M'):
                        time_span = f"ca. kl. {start_time.strftime('%H:%M')}"
                    else:
                        time_span = f"i perioden ca. kl. {start_time.strftime('%H:%M')} - {end_time.strftime('%H:%M')}"

                    if outside_working_time:
                        bullet_text = (
                            f"- {j - i} overskridelser {weekday.lower()} den {start_time.day}. {month_danish(start_time.month)} {start_time.year} "
                            f"{time_span}. "
                            f"Maksimalt vibrationsniveau {max_vibration} mm/s ved {frequency} Hz. "
                            f"Det bemærkes at hændelserne er sket udenfor entreprenørens normale arbejdstid."
                            f"Arbejdet er formentligt udført tæt på måleren, hvorfor det vurderes at vibrationsniveauet ikke afspejler den generelle påvirkning af ejendommen. \n"
                        )
                    else:
                        bullet_text = (
                            f"- {j - i} overskridelser {weekday.lower()} den {start_time.day}. {month_danish(start_time.month)} {start_time.year} "
                            f"{time_span}. "
                            f"Maksimalt vibrationsniveau {max_vibration} mm/s ved {frequency} Hz. "
                            f"Arbejdet er formentligt udført tæt på måleren, hvorfor det vurderes at vibrationsniveauet ikke afspejler den generelle påvirkning af ejendommen. \n"
                        )
                
                # Write the bullet to the file
                file.write(bullet_text)
                i = j  # Move to the next group of events

        if events_above_5 != {}:
            text_path = os.path.join(main_text_path, "Overskridelser_over_5.md")
            with open(text_path, 'r', encoding='utf-8') as file:
                text = file.read()
                
            text = text.replace("HÆNDELSE/HÆNDELSER", "hændelse" if Reel + Arbe == 1 else "hændelser")
            
            text_final_file = os.path.join(text_final_path,"text_3.md")
            with open(text_final_file, 'w', encoding='utf-8') as file:
                file.write(text)
            
                # Process and format each date's events
                for date_event, events in events_above_5.items():
                    
                    events.sort(key=lambda x: x['datetime'])  # Sort by datetime within each day
                    
                    holidays_event_year = Denmark(date_event.year)
                    custom_holidays = {
                        date(date_event.year, 12, 24): "Christmas Eve",
                        date(date_event.year, 12, 31): "New Years Eve"
                    }

                    holidays_event_year.update(custom_holidays)

                    i = 0
                    while i < len(events):
                        start_event = events[i]
                        start_time = start_event['datetime']
                        max_vibration = start_event['max_vibration']
                        frequency = start_event['frequency']
                        vib_type = start_event["type"]
                        
                        is_weekday = start_time.weekday() < 5
                        is_working_hour = 6<= start_time.hour < 17
                        is_not_holiday = start_time.date() not in holidays_event_year

                        outside_working_time = not (is_weekday and is_working_hour and is_not_holiday)
                        # Find the end of the time window
                        j = i + 1
                        while j < len(events) and (events[j]['datetime'] - start_time) <= max_time_delta and vib_type == events[j]["type"]:
                            # Update max vibration, frequency, and direction if a higher value is found
                            if events[j]['max_vibration'] > max_vibration:
                                max_vibration = events[j]['max_vibration']
                                frequency = events[j]['frequency']
                            j += 1

                        if j - i == 1 and vib_type == 1:
                            if outside_working_time:
                                # Single transient
                                bullet_text = (
                                    f"- {weekday_danish(start_time.weekday())} den {start_time.day}. {month_danish(start_time.month)} {start_time.year} "
                                    f"ca. kl. {start_time.strftime('%H:%M')}. Maksimal vibrationsniveau {max_vibration} mm/s ved {frequency} Hz. " 
                                    "Det bemærkes at hændelserne er sket udenfor entreprenørens normale arbejdstid.\n"
                                )
                            else:
                                # Single transient
                                bullet_text = (
                                    f"- {weekday_danish(start_time.weekday())} den {start_time.day}. {month_danish(start_time.month)} {start_time.year} "
                                    f"ca. kl. {start_time.strftime('%H:%M')}. Maksimal vibrationsniveau {max_vibration} mm/s ved {frequency} Hz.\n"
                                )
                        elif j - i == 1 and vib_type == 3:
                            if outside_working_time:
                                # Single transient
                                bullet_text = (
                                    f"- {weekday_danish(start_time.weekday())} den {start_time.day}. {month_danish(start_time.month)} {start_time.year} "
                                    f"ca. kl. {start_time.strftime('%H:%M')}. Maksimal vibrationsniveau {max_vibration} mm/s ved {frequency} Hz.  " 
                                    f"Det bemærkes at hændelserne er sket udenfor entreprenørens normale arbejdstid."
                                    f"Arbejdet er formentligt udført tæt på måleren, hvorfor det vurderes at vibrationsniveauet ikke afspejler den generelle påvirkning af ejendommen. \n"
                                )
                            else:
                                bullet_text = (
                                    f"- {weekday_danish(start_time.weekday())} den {start_time.day}. {month_danish(start_time.month)} {start_time.year} "
                                    f"ca. kl. {start_time.strftime('%H:%M')}. Maksimal vibrationsniveau {max_vibration} mm/s ved {frequency} Hz. " 
                                    f"Arbejdet er formentligt udført tæt på måleren, hvorfor det vurderes at vibrationsniveauet ikke afspejler den generelle påvirkning af ejendommen. \n"
                                )
                        elif j - i != 1 and vib_type == 1:
                            # Multiple transients within time window
                            end_time = events[j - 1]['datetime']
                            weekday = weekday_danish(start_time.weekday())

                            if start_time.strftime('%H:%M') == end_time.strftime('%H:%M'):
                                time_span = f"ca. kl. {start_time.strftime('%H:%M')}"
                            else:
                                time_span = f"i perioden ca. kl. {start_time.strftime('%H:%M')} - {end_time.strftime('%H:%M')}"
                            
                            if outside_working_time:
                                bullet_text = (
                                    f"- {j - i} overskridelser {weekday.lower()} den {start_time.day}. {month_danish(start_time.month)} {start_time.year} "
                                    f"{time_span}. "
                                    f"Maksimalt vibrationsniveau {max_vibration} mm/s ved {frequency} Hz. "
                                    f"Det bemærkes at hændelserne er sket udenfor entreprenørens normale arbejdstid. \n"
                                )
                            else:
                                bullet_text = (
                                    f"- {j - i} overskridelser {weekday.lower()} den {start_time.day}. {month_danish(start_time.month)} {start_time.year} "
                                    f"{time_span}. "
                                    f"Maksimalt vibrationsniveau {max_vibration} mm/s ved {frequency} Hz.\n"
                                )
                        elif j - i != 1 and vib_type == 3:
                            # Multiple transients within time window
                            end_time = events[j - 1]['datetime']
                            weekday = weekday_danish(start_time.weekday())

                            if start_time.strftime('%H:%M') == end_time.strftime('%H:%M'):
                                time_span = f"ca. kl. {start_time.strftime('%H:%M')}"
                            else:
                                time_span = f"i perioden ca. kl. {start_time.strftime('%H:%M')} - {end_time.strftime('%H:%M')}"
                                
                            if outside_working_time:
                                bullet_text = (
                                    f"- {j - i} overskridelser {weekday.lower()} den {start_time.day}. {month_danish(start_time.month)} {start_time.year} "
                                    f"{time_span}. "
                                    f"Maksimalt vibrationsniveau {max_vibration} mm/s ved {frequency} Hz. "
                                    f"Det bemærkes at hændelserne er sket udenfor entreprenørens normale arbejdstid."
                                    f"Arbejdet er formentligt udført tæt på måleren, hvorfor det vurderes at vibrationsniveauet ikke afspejler den generelle påvirkning af ejendommen. \n"
                                )
                            else:
                                bullet_text = (
                                    f"- {j - i} overskridelser {weekday.lower()} den {start_time.day}. {month_danish(start_time.month)} {start_time.year} "
                                    f"{time_span}. "
                                    f"Maksimalt vibrationsniveau {max_vibration} mm/s ved {frequency} Hz. "
                                    f"Arbejdet er formentligt udført tæt på måleren, hvorfor det vurderes at vibrationsniveauet ikke afspejler den generelle påvirkning af ejendommen. \n"
                                )
                        
                        # Write the bullet to the file
                        file.write(bullet_text)
                        i = j  # Move to the next group of events
        elif events_above_5 == {} and limit != 5:
            text_path = os.path.join(main_text_path, "Overskridelser_under_5.md")
            with open(text_path, 'r', encoding='utf-8') as file:
                text = file.read()
                
            text = text.replace("HÆNDELSEN/HÆNDELSERNE", "hændelsen" if Reel + Arbe == 1 else "hændelserne")
            
            text_final_file = os.path.join(text_final_path,"text_3.md")
            with open(text_final_file, 'w', encoding='utf-8') as file:
                file.write(text)

def create_result_text(cache_main_dir):
    from basic_functions import remove_all_files
    from basic_functions import load_json
    import string
    import os

    drive = "O:"
    files_path = os.path.join("A000000", "A004371", "3_Pdoc", "Afrapportering", "files")
    files_path = os.path.normpath(drive + os.sep + files_path)
    trans_dict = load_json(os.path.join(cache_main_dir,"Results","trans_dict_final.json"))
    info_dict = load_json(os.path.join(cache_main_dir, "API","project_sensor_dict_final.json"))
    data_dict = load_json(os.path.join(cache_main_dir,"Results","max_data.json"))

    for i, (adresse, details) in enumerate(trans_dict.items()):
        main_text_path = os.path.join(files_path,"Tekst","Måleresultater", info_dict[adresse]["logger"])
        sensor_id = str(info_dict[adresse]["sensor_id"])
        text_final_path = os.path.join(cache_main_dir,"Rapport","Tekst",f"{adresse}")

        os.makedirs(text_final_path, exist_ok=True)

        remove_all_files(text_final_path)

        data = data_dict[adresse]
        Reel = details['Reel']
        Slag = details['Slag']
        Arbe = details['Arbe']

        limit = info_dict[adresse]["limit"]
        bygningstype = "vibrationsfølsomme" if limit == 3 else "normale"

        n_trans = Reel + Slag + Arbe
        Bilag = string.ascii_uppercase[i]
        
        if info_dict[adresse]["logger"] != "V12":
        
            if all(val == 0 for val in [Reel, Slag, Arbe]):
        
                text_path = os.path.join(main_text_path, "Ingen_overskridelser.md")
                with open(text_path, 'r', encoding='utf-8') as file:
                    text = file.read()
                
                text = text.replace("BILAG_FLAG",f"{Bilag}")
                text = text.replace("VIBRATIONS_FLAG",f"{str(float(data['vibration'])).replace('.', ',')}")
                text = text.replace("FREQ_FLAG",f"{str(float(data['frequency'])).replace('.', ',')}")
                text = text.replace("PER_FLAG",f"{str(float(data['percentage'])).replace('.', ',')}")
                text = text.replace("VIB_ELLER_NORMAL", bygningstype)

                text_final_file = os.path.join(text_final_path,"text_1.md")
                with open(text_final_file, 'w', encoding='utf-8') as file:
                    file.write(text)

            elif Slag != 0 and Reel == 0 and Arbe == 0:
                text_path = os.path.join(main_text_path, "Ingen_overskridelser_men_stoed.md")
                with open(text_path, 'r', encoding='utf-8') as file:
                    text = file.read()
                
                text = text.replace("BILAG_FLAG",f"{Bilag}")
                text = text.replace("N_FLAG",f"{n_trans}")
                text = text.replace("OVERSKRIDELSER/OVERSKRIDELSE", "overskridelse" if n_trans == 1 else "overskridelser")
                text = text.replace("OVERSKRIDELSEN/OVERSKRIDELSERNE", "overskridelsen" if n_trans == 1 else "overskridelserne")
                text = text.replace("DEN/DE", "den" if n_trans == 1 else "de")
                text = text.replace("VIBRATIONS_FLAG",f"{str(float(data['vibration'])).replace('.', ',')}")
                text = text.replace("FREQ_FLAG",f"{str(float(data['frequency'])).replace('.', ',')}")
                text = text.replace("PER_FLAG",f"{str(float(data['percentage'])).replace('.', ',')}")
                text = text.replace("VIB_ELLER_NORMAL", bygningstype)
                
                text_final_file = os.path.join(text_final_path,"text_1.md")
                with open(text_final_file, 'w', encoding='utf-8') as file:
                    file.write(text)

            elif Slag == 0 and (Reel != 0 or Arbe != 0):
                text_path = os.path.join(main_text_path, "Overskridelser_ingen_stoed.md")
                with open(text_path, 'r', encoding='utf-8') as file:
                    text = file.read()
                
                text = text.replace("BILAG_FLAG",f"{Bilag}")
                text = text.replace("N_FLAG",f"{n_trans}")
                text = text.replace("OVERSKRIDELSE/OVERSKRIDELSER","overskridelse" if Reel + Arbe == 1 else "overskridelser")
                text = text.replace("HÆNDELSEN/HÆNDELSERNE","Hændelsen" if Reel + Arbe == 1 else "Hændelserne")
                text = text.replace("VIB_ELLER_NORMAL", bygningstype)
                
                text_final_file = os.path.join(text_final_path,"text_1.md")
                with open(text_final_file, 'w', encoding='utf-8') as file:
                    file.write(text)
                
                generate_transient_report(details, main_text_path, text_final_path, sensor_id, Reel, Arbe, bygningstype, limit)

            elif Slag != 0 and (Reel != 0 or Arbe != 0):
                text_path = os.path.join(main_text_path, "Overskridelser_men_stoed.md")
                with open(text_path, 'r', encoding='utf-8') as file:
                    text = file.read()
                
                text = text.replace("BILAG_FLAG",f"{Bilag}")
                text = text.replace("N_FLAG",f"{n_trans}")
                text = text.replace("OVERSKRIDELSER/OVERSKRIDELSE", "overskridelse" if n_trans == 1 else "overskridelser")
                text = text.replace("N_SLAG_FLAG",f"{Slag}")
                text = text.replace("OVERSKRIDELSE/OVERSKRIDELSER", "overskridelse" if Slag == 1 else "overskridelser")
                text = text.replace("DEN/DE_SLAG", "den" if Slag == 1 else "de")
                text = text.replace("DEN/DE_REEL", "Den" if (Reel + Arbe) == 1 else "De")
                text = text.replace("HÆNDELSE/HÆNDELSER_REEL", "hændelse" if (Reel + Arbe) == 1 else "hændelser")
                text = text.replace("VIB_ELLER_NORMAL", bygningstype)
                
                
                text_final_file = os.path.join(text_final_path,"text_1.md")
                with open(text_final_file, 'w', encoding='utf-8') as file:
                    file.write(text)
                
                generate_transient_report(details, main_text_path, text_final_path, sensor_id, Reel, Arbe, bygningstype, limit)
        else:
            if all(val == 0 for val in [Reel, Slag, Arbe]):
                text_path = os.path.join(main_text_path, "Ingen_overskridelser.md")
                with open(text_path, 'r', encoding='utf-8') as file:
                    text = file.read()
                
                text = text.replace("BILAG_FLAG",f"{Bilag}")
                text = text.replace("VIBRATIONS_FLAG",f"{str(float(data['vibration'])).replace('.', ',')}")
                text = text.replace("PER_FLAG",f"{str(float(data['percentage'])).replace('.', ',')}")
                text = text.replace("VIB_ELLER_NORMAL", bygningstype)

                text_final_file = os.path.join(text_final_path,"text_1.md")
                with open(text_final_file, 'w', encoding='utf-8') as file:
                    file.write(text)

            elif Slag != 0 and Reel == 0 and Arbe == 0:
                text_path = os.path.join(main_text_path, "Ingen_overskridelser_men_stoed.md")
                with open(text_path, 'r', encoding='utf-8') as file:
                    text = file.read()
                
                text = text.replace("BILAG_FLAG",f"{Bilag}")
                text = text.replace("N_FLAG",f"{n_trans}")
                text = text.replace("LIMIT_FLAG",f"{limit}")
                text = text.replace("OVERSKRIDELSER/OVERSKRIDELSE", "overskridelse" if n_trans == 1 else "overskridelser")
                text = text.replace("OVERSKRIDELSEN/OVERSKRIDELSERNE", "overskridelsen" if n_trans == 1 else "overskridelserne")
                text = text.replace("DEN/DE", "den" if n_trans == 1 else "de")
                text = text.replace("VIBRATIONS_FLAG",f"{str(float(data['vibration'])).replace('.', ',')}")
                text = text.replace("PER_FLAG",f"{str(float(data['percentage'])).replace('.', ',')}")
                text = text.replace("VIB_ELLER_NORMAL", bygningstype)
                
                text_final_file = os.path.join(text_final_path,"text_1.md")
                with open(text_final_file, 'w', encoding='utf-8') as file:
                    file.write(text)

            elif Slag == 0 and (Reel != 0 or Arbe != 0):
                text_path = os.path.join(main_text_path, "Overskridelser_ingen_stoed.md")
                with open(text_path, 'r', encoding='utf-8') as file:
                    text = file.read()
                
                text = text.replace("BILAG_FLAG",f"{Bilag}")
                text = text.replace("N_FLAG",f"{n_trans}")
                text = text.replace("OVERSKRIDELSE/OVERSKRIDELSER","overskridelse" if Reel + Arbe == 1 else "overskridelser")
                text = text.replace("LIMIT_FLAG",f"{limit}")
                text = text.replace("HÆNDELSEN/HÆNDELSERNE","Hændelsen" if Reel + Arbe == 1 else "Hændelserne")
                text = text.replace("VIB_ELLER_NORMAL", bygningstype)
                
                text_final_file = os.path.join(text_final_path,"text_1.md")
                with open(text_final_file, 'w', encoding='utf-8') as file:
                    file.write(text)
                
                generate_transient_report(details, main_text_path, text_final_path, sensor_id, Reel, Arbe, bygningstype, limit)

            elif Slag != 0 and (Reel != 0 or Arbe != 0):
                text_path = os.path.join(main_text_path, "Overskridelser_men_stoed.md")
                with open(text_path, 'r', encoding='utf-8') as file:
                    text = file.read()
                
                text = text.replace("BILAG_FLAG",f"{Bilag}")
                text = text.replace("N_FLAG",f"{n_trans}")
                text = text.replace("OVERSKRIDELSER/OVERSKRIDELSE", "overskridelse" if n_trans == 1 else "overskridelser")
                text = text.replace("LIMIT_FLAG",f"{limit}")
                text = text.replace("N_SLAG_FLAG",f"{Slag}")
                text = text.replace("OVERSKRIDELSE/OVERSKRIDELSER", "overskridelse" if Slag == 1 else "overskridelser")
                text = text.replace("DEN/DE_SLAG", "den" if Slag == 1 else "de")
                text = text.replace("DEN/DE_REEL", "Den" if (Reel + Arbe) == 1 else "De")
                text = text.replace("HÆNDELSE/HÆNDELSER_REEL", "hændelse" if (Reel + Arbe) == 1 else "hændelser")
                text = text.replace("VIB_ELLER_NORMAL", bygningstype)
                
                
                text_final_file = os.path.join(text_final_path,"text_1.md")
                with open(text_final_file, 'w', encoding='utf-8') as file:
                    file.write(text)
                
                generate_transient_report(details, main_text_path, text_final_path, sensor_id, Reel, Arbe, bygningstype, limit)





#cache_main_dir = "O:\\A000000\\A004371\\3_Pdoc\\Afrapportering\\A223276-094 - Bakkelygade m.fl., Nørresundby"
#create_result_text(cache_main_dir)
#create_transient_plots(cache_main_dir)