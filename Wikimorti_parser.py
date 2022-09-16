import json

import wikipediaapi


def main():
    wiki_wiki = wikipediaapi.Wikipedia('en', extract_format=wikipediaapi.ExtractFormat.WIKI)
    path = 'Deaths_in_'
    years = [str(y) for y in range(1998, 2022)]
    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July',
              'September', 'October', 'November', 'December']
    total_data = {}
    for year in years:
        total_data[year] = {}
        for month in months:
            print("Processing: " + year, month + "...")
            # open the wiki page at that month + year
            page_py = wiki_wiki.page(path + month + '_' + year)

            # save the parsed wiki page in to a dictionary
            monthly_deaths_by_day = parse_page(page_py.text)
            total_data[year][month] = monthly_deaths_by_day

    """for key, value in famous_deaths.items():
        print(str(key) + ':', value)"""

    """pprint(total_data, 3)"""
    with open("deadge.json", 'w') as f:
        json.dump(total_data, f, indent=3)



def parse_page(text):
    # find where the line with deaths starts: month + year
    # find the day number
    # parse all the lines after until a new number alone
    deaths_by_day = {}
    day = 0

    text_splitted = text.split('\n')
    for line in text_splitted:
        if line.isdigit():
            if int(line.strip(" ")) >= day:
                day += 1
                deaths_by_day[day] = []
        elif line != "" and line != '== References ==':
            if day in deaths_by_day:
                parsed_line = parse_line(line)
                if parsed_line:
                    deaths_by_day[day].append(parsed_line)

    return deaths_by_day


def parse_line(line):
    line_splitted = line.split(',')
    line_parsed = {"name": line_splitted[0].strip()}
    try:
        try:
            line_parsed["age"] = int(line_splitted[1].strip().split("-")[0])
        except ValueError as e:
            print("Error line:", line)
            return None
    except IndexError as e:
        print("Error line:", line)
        return None
    try:
        line_parsed["info"] = line_splitted[2:]
    except IndexError as e:
        return None

    return line_parsed


def pprint(obj, i):
    print(json.dumps(obj, indent=i))


if __name__ == '__main__':
    main()
