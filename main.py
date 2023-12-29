from functions import *

run = True

while run: 
    print_logo()
    choice = input(COLORS.BLUE + "1" + COLORS.RESET + ". Analyze a Reddit post\\ " + COLORS.BLUE + "2" + COLORS.RESET + ". Analyze your own text \\" + COLORS.BLUE + "3" + COLORS.RESET + ". Exit\n")
    while choice not in ["1", "2", "3"]:
        print(COLORS.RED + "Invalid " + COLORS.RESET + "choice. Please try again.")
        choice = input("")
    if choice == "1":
        clear_screen()
        runReddit = True
        print_logo()
        while runReddit:
            url = input("Enter the URL of the " + COLORS.RED + "Reddit " + COLORS.RESET + "post: ")
            platform = get_platform(url)
            if platform == 'reddit':
                title, body = get_reddit_post_text(url)
                clean_title = clean_text(title)
                clean_body = clean_text(body)
                print(COLORS.BLUE + "POST PREVIEW:" + COLORS.RESET)
                print(COLORS.PURPLE + "Title: " + COLORS.RESET + clean_title)
                print(COLORS.PURPLE + "Body: " + COLORS.RESET + clean_body)
                feeling = get_sentiment(clean_body)
                print("\n")
                print("AI feels that this post is: " + COLORS.BLUE + feeling + COLORS.RESET)
                get_language(clean_body)
                repeat_prompt = "Would you like to analyze another text? (" + COLORS .GREEN + "y" + COLORS.RESET + "/" + COLORS.RED + "n" + COLORS.RESET + ")"
                repeat = ask_repeat_analysis(repeat_prompt)

                if repeat == "y":
                    clear_screen()
                    print_logo()
                    continue
                else:
                    runReddit = False
                    clear_screen()
                    continue
            elif platform == 'unknown':
                print(COLORS.RED + "Sorry" + COLORS.RESET + ", that's not a " + COLORS.RED + "Reddit " + COLORS.RESET + "post: ")
                continue
    elif choice == "2":
        clear_screen()
        runText = True
        while runText:
            print_logo()
            text = input("Enter the text you would like to analyze: ")
            clean_output = clean_text(text)
            feeling = get_sentiment(clean_output)
            print("\n")
            print("AI feels that this text is: " + COLORS.BLUE + feeling + COLORS.RESET)
            get_language(clean_output)
            repeat_prompt = "Would you like to analyze another text? (" + COLORS .GREEN + "y" + COLORS.RESET + "/" + COLORS.RED + "n" + COLORS.RESET + ")"
            repeat = ask_repeat_analysis(repeat_prompt)

            if repeat == "y":
                clear_screen()
                continue
            else:
                runText = False
                clear_screen()
                continue
    elif choice == "3":
        run = False
        continue