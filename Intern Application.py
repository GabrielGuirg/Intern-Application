import string
import json
import datetime

class Student:
    def __init__(self, name, email, password, membership_type):
        self.name = name
        self.email = email
        self.password = password
        self.membership_type = membership_type
        self.is_active = True
        self.last_payment_date = None
        self.messages = []
        self.notifications = []
        self.notificationCount = 0

    def send_message(self, recipient, message):
        if self.is_active:
            if recipient.is_active:
                recipient.receive_message(self, message)
            else:
                print(f"Sorry, {recipient.name} is not currently an active member.")
        else:
            print("Sorry, you need to be an active member to send messages.")

    def receive_message(self, sender, message):
        self.messages.append((sender, message))
        self.notificationCount += 1

class InCollege:
    STANDARD_MEMBERSHIP = "standard"
    PLUS_MEMBERSHIP = "plus"
    PLUS_MEMBERSHIP_FEE = 10.0

    def __init__(self):
        self.students = []

    def register_student(self, name, email, password, membership_type):
        student = Student(name, email, password, membership_type)
        self.students.append(student)

    def login_student(self, email, password):
        for student in self.students:
            if student.email == email and student.password == password:
                return student
        return None


    def select_membership_type(self):
        while True:
            membership_type = input("Select your membership type (standard/plus): ").lower()
            if membership_type in [self.STANDARD_MEMBERSHIP, self.PLUS_MEMBERSHIP]:
                return membership_type
            else:
                print("Invalid membership type. Please try again.")

    def charge_membership_fee(self, student):
        if student.membership_type == self.PLUS_MEMBERSHIP and student.is_active:
            # Charge the student
            # Here we're just updating the last payment date, but in a real implementation
            # you would use a payment gateway to charge the student's credit card
            if student.last_payment_date is None or (datetime.datetime.now() - student.last_payment_date).days >= 30:
                # Charge the student $10
                student.last_payment_date = datetime.datetime.now()
                print(f"Billed {student.name} $10 for plus membership.")

    def check_membership_status(self, student):
        if student.membership_type == self.PLUS_MEMBERSHIP:
            # Check if the student's membership is still active
            # Here we're just checking if it's been less than a month since the last payment,
            # but in a real implementation you would use a payment gateway to verify the student's
            # credit card and check if the payment is still being processed
            if student.last_payment_date is None or (datetime.datetime.now() - student.last_payment_date).days >= 30:
                student.is_active = False

    def get_all_students(self, student):
        if student.membership_type == self.PLUS_MEMBERSHIP and student.is_active:
            for s in self.students:
                print(s.name)

class Friend:
    def __init__(self, friendList) -> None:
        self.friendList = friendList
        self.membership = InCollege.check_membership_status()
        
    def check_send_req(self, recipent, message):
        if recipent in self.friendList:
            Student.send_message(recipent, message)
        elif (self.membership == "plus"):
            Student.send_message(recipent, message)
        else:
            print("I'm sorry, you are not friends with that person")

class Inbox:
    def __init__(self, sender, message, messagelist):
        self.sender = sender
        self.message = message
        self.messageList = messagelist
    
    def notification(self):
        if Student.receive_message:
            print("message Recieved")

    def deleteMessage(self, message):
        self.messageList.remove(message)
        
    def respond(self, message):
        Friend.check_send_req(self.sender, message)
        

class JobPost(object):
    def __init__(self, title, desc, employer, location, salary):
        self.title = title
        self.desc = desc
        self.employer = employer
        self.location = location
        self.salary = salary
        self.applicants = []

    def delete_job(self, accounts):
        notif = "A job that you applied for has been deleted."
        del accounts[self.employer]["Jobs"][self.title]
        for applicant in self.applicants:
            if applicant in accounts:
                if self.title in accounts[applicant]["Notifications"]:
                    accounts[applicant]["Notifications"].remove(self.title)
                    appendGeneralNotifications(accounts, applicant, notif)
        print("Job was deleted and the notifications were removed.")


def appendGeneralNotifications(account, student, notif):
    name = account[student]["First Name"] + " " + account[student]["Last Name"]

    for student in students:                                                                            #IDK where the students class is stored (Manthan) - Need to fix this
        if student.name == name:
            student.notifications.append(notif)
            student.notificationCount += 1


def set_firstname():
    name = input("Enter first name: ")
    return name

def set_lastname():
    name = input("Enter last name: ")
    return name

def set_university():
    university = input("What university do you attend?: ")
    return university

def set_major():
    major = input("What are you majoring in?: ")
    return major

def update_uni_or_major(accounts, username):
    university = input("What university do you attend?: ")
    major = input("What are you majoring in?: ")
    accounts[username]["University"] = university
    accounts[username]["Major"] = major
    return accounts

def set_users_password(username, accounts):
    password = input("Enter desired password: ")
    special_symb = set(string.punctuation)
    if len(password) < 8:
        print("Length of password must be at least 8 characters.\n")
        set_users_password(username, accounts)

    elif len(password) > 12:
        print("Length of password must be less than 12 characters.\n")
        set_users_password(username, accounts)

    elif not any(char.isupper() for char in password):
        print("Password must contain at least one capital letter.\n")
        set_users_password(username, accounts)

    elif not any(char.islower() for char in password):
        print("Password must contain at least one lower case letter.\n")
        set_users_password(username, accounts)
    elif not any(char.isdigit() for char in password):
        print("Password must contain at least one digit.\n")
        set_users_password(username, accounts)

    elif not any(char in special_symb for char in password):
        print("Password must contain at least one special character.\n")
        set_users_password(username, accounts)
    else:
        days_since_last_applied = 0
        firstname = set_firstname()  # getting first name
        lastname = set_lastname()  # getting last name
        university = set_university()   # getting university
        major = set_major() # getting major
        accounts[username] = {"Password": password, "First Name": firstname, "Last Name": lastname, "University": university,
                              "Major": major, "Language": "English",
                              "Requests": {"Name": "", "University": "", "Major": ""},
                              "Jobs Applied" : {"Job": "", "Graduation":"", "Start": "", "Description": "",
                                                "Days since last applied :": days_since_last_applied},
                              "Jobs Saved" : []}
    return accounts

def checkProfileCration(account, username):
    profile = loadProfile()
    if profile[username] == account[username]:
        return 0
    else:
        return 1


def success_login(account, username):
    print("Options to search for a job/internship, find someone that they know, learn a new skill, update account info, or delete a job.")
    if account[username]["Jobs Applied"]["Days since last applied"] == 7:
        notify = "Remember – you're going to want to have a job when you graduate. Make sure that you start to apply for jobs today!"
        appendGeneralNotifications(account, username, notify)

    if checkProfileCration(account, username) == 1:
        notify = "Don't forget to create a profile"
        appendGeneralNotifications(account, username, notify)

    selection = input("Type J for job/intership, S for searching someone, L for learning a skill, U to update your account information,"
                      " D to delete a job, N for your notifications, or V to view all jobs: ")
    if selection == "J":
        post_job(account, username)
        success_login(account, username)

    elif selection == "D":
        job_title = input("Enter the title of the job to delete: ")
        if job_title in account[username]["Jobs"]: 
            account[username]["Jobs"][job_title].delete_job(account)
        else:
            print("Job not found.")
    
    elif selection == "S":
        search_user_by_name(account, username)
        success_login(account, username)
    elif selection == "L":
        skillChoice = input("Would you like to select a skill? yes or no: ")

    elif selection == "V":
        if len(account[username]["Jobs Applied"]) != 0:
            numberofjobsapplied = "You have applied for %d jobs", len(account[username]["Jobs Applied"])
            appendGeneralNotifications(account, username, numberofjobsapplied)

        for employer, employer_data in account.items():
            if "Jobs" in employer_data:
                for job_title, job in employer_data["Jobs"].items():
                    print(job_title)

        job_title = input("Enter the title of the job to display: ")
        for employer, employer_data in account.items():
            if "Jobs" in employer_data:
                if job_title in employer_data["Jobs"]:
                    job = employer_data["Jobs"][job_title]
                    print(f"Title: {job.title}")
                    print(f"Description: {job.desc}")
                    print(f"Employer: {job.employer}")
                    print(f"Location: {job.location}")
                    print(f"Salary: {job.salary}")
                    break

        skillChoice = input("Would you like to select a skill? yes or no: ")
        while skillChoice == "yes":
            skill = input(
                "Learn a new skill (Type the following skill):\n 1.) Communication \n 2.) Program \n "
                "3.) Self-Management \n 4.) Writing \n 5.) Public Speaking\n\n")
            if skill == "Communication":
                print("Under construction")
                break
            elif skill == "Program":
                print("Under construction")
                break
            elif skill == "Self-Management":
                print("Under construction")
                break
            elif skill == "Writing":
                print("Under Construction")
                break
            elif skill == "Public Speaking":
                print("Under Construction")
                break
            else:
                print("Invalid skill selected. Please try again.")
                skillChoice = input("Would you like to select a skill? yes or no: ")
        if skillChoice == "no":
            print()
            main()
    elif selection == "U":
        update_uni_or_major(account, username)
    else:
        print("Invalid selection. Please try again.")

def existing_account(accounts):
    username = input("Enter existing username: ")
    if username in accounts.keys():
        print(accounts[username]['Password'])
        password = input("Enter password: ")
        if accounts[username]['Password'] != password:
            print("Incorrect username/password, please try again.")
            existing_account(accounts)
        else:
            success_login(accounts, username)
    else:
        print("There is no account with the inserted username. Please try again.\n")
        main()

def new_account(accounts):
    username = input("Enter new username: ")
    if username in accounts.keys():
        print("Username already exists.")
        new_account(accounts)  # added because if username given already says write a new that does not exist
        existing_account(accounts)
    else:
        accounts = set_users_password(username, accounts)
        with open('Information.json', 'w') as file:
            file.write(json.dumps(accounts))
        print("Account created successfully.\n")
        success_login(accounts, username)

    notifyOtherStudents = "%s %s has joined InCollege", accounts[username]["First Name"], accounts[username]["First Name"]
    for user in accounts:
        if user != accounts[username]
            appendGeneralNotifications(accounts, user, notifyOtherStudents)

def loadFile():
    try:
        f = open("Information.json")
        return json.load(f)
    except Exception as e:
        return {}
        
def search_user_by_name(accounts, username):
    l_name = input("Enter last name of user (Or enter R to return to previous menu):")
    if l_name == "R":
        return
    f_name = input("Enter first name of user: ")
    for user in accounts:
        for a in accounts[user]:
            if l_name in accounts[user]['Last Name']:
                if f_name in accounts[user]['First Name']:
                    print("They are a part of the InCollege")
                    add = input("Do you want to add them as a friend? (y/n): ")
                    if add == "y":
                        add_name = accounts[user]['First Name'] + accounts[user]['Last Name']
                        add_uni = accounts[user]['University']
                        add_major = accounts[user]['Major']
                        d_addUser = {"Name": add_name, "University": add_uni, "Major": add_major}
                        accounts[username]["Requests"].update(Name = add_name, University = add_uni, Major = add_major)
                        print("Name to add" + add_name + "\n")
                        print("University to add" + add_uni + "\n")
                        print(("Name to add" + add_major + "\n"))
                        return
                    else:
                        return

    print("They are not yet a part of the InCollege System")
    search_user_by_name(accounts, username)

def post_job(account, username):
    title = input("Title: ")
    desc = input("Job Description: ")
    employer = input("Employer Name: ")
    loc = input("Enter Location: ")
    salary = input("Enter Salary: ")
    account[username]['Job'] = JobPost(title, desc, employer, loc, salary)
    newJobPostNotif = "A new job, %s, has been posted", title
    for user in account:
        if user != account[username]:
            appendGeneralNotifications(account, user, newJobPostNotif)
    with open('Information.json', 'w') as file:
        file.write(json.dumps(account))

def useful_links():
    link_selection = input("Select the link to access:\n"
                            "General (G) | Browse InCollege (B) | Business Solutions (S) | Directories (D): ")
    if link_selection == "G":
        selection_general()
    elif link_selection == "B":
        selection_BI()
    elif link_selection == "S":
        selection_BS()
    elif link_selection == "D":
        selection_directories()
    else:
        print("Invalid selection!")
        useful_links()

def selection_general():
    gen_links = input("Please select from following links:\n"
                      "Sign Up (S) | Help Center (H) | About (A) | Press (P) | Blog (B) | Careers (C) |"
                      " Developers (D) (To Return to previous menu enter 'R'): ")
    if gen_links == "S":
        account_type = input("\nDo you wish to create a new InCollege account or log into existing account?\n"
                                 "(Insert N for new account or E for existing account)\n"
                                 "(To return to previous menu, enter 'R'): ")
        accounts = loadFile()

        if account_type == "N":
            if len(accounts.keys()) == 10:
                print("All permitted accounts have ben created, please come back later.\n")
            new_account(accounts)
        elif account_type == "E":
            existing_account(accounts)
        else:
            print("Invalid input.\n")
            selection_general()

    elif gen_links == "H":
        print("We're here to help!\n")
        return
    elif gen_links == "A":
        print("In College: Welcome to In College, the world's largest college student "
              "network with many users in many countries and territories worldwide.\n")
        return
    elif gen_links == "P":
        print("In College Pressroom: Stay on top of the latest news, updates, and reports.\n")
        return
    elif gen_links == "B":
        print("Under Construction.\n")
        return
    elif gen_links == "C":
        print("Under Construction.\n")
        return
    elif gen_links == "D":
        print("Under Construction.\n")
        return
    elif gen_links == "R":
        return
    else:
        print("Invalid input.\n")
        selection_general()

def selection_BI():
    print("Under Construction")
    return

def selection_BS():
    print("Under Construction")
    return

def selection_directories():
    print("Under Construction")
    return

def important_links():
    imp_links = input("Please select one of the following links:\nCopyright Notice(CN) | About (A) | Accessibility(AB) | "
              "User Agreement (UA) | Privacy Policy (PP) | Cookie Policy (CP) | Copyright Policy (CY) | Brand Policy (BP): ")
    if imp_links == "CN":
        print("Under Construction")
        return
    if imp_links == "A":
        print("Under Construction")
        return
    if imp_links == "AB":
        print("Under Construction")
        return
    if imp_links == "UA":
        print("Under Construction")
        return
    if imp_links == "PP":
        guest_controls = input("To access Guest Controls, enter 'GC': ")
        if guest_controls == "GC":
            turn_off_sub = input(
                "Would you like to turn off subscription to our mailing list, SMS Texts, and Targeted Ad features?"
                "(Y for yes, or 'N' for no): ")
            if turn_off_sub == "Y" or "y":
                return
            return
        return
    if imp_links == "CP":
        print("Under Construction")
        return
    if imp_links == "CY":
        print("Under Construction")
        return
    if imp_links == "BP":
        print("Under Construction")
        return
    else:
        print("Invalid selection! Please try again.\n")
        important_links()

def language():
    set_language = input("Choose your language ('E' for English or 'S' for Spanish): ")
    if set_language == "E":
        return
    if set_language == "S":
        print("Language set to Spanish")
        return

def loadProfile():
    try:
        f = open("profile.json")
        return json.load(f)
    except Exception as e:
        return {}

def creating_all_profiles(accounts, profile):

    for user in accounts.key():
        profile[user]= {"title": "",
                         "Major": "",
                         "University": "",
                         "information": "",
                         "experience": {},
                         "education": {}}
        with open('Ptofile.json', 'w') as file:
            try:
                file.write(json.dumps(profile))
            except json.decoder.JSONDecodeError:
                print("This is an error.")

def create_profile(account, username, profile):
    profile_choice = str(input("Do you wish to write your profile (w), continue where you left off (c), view your profile (v) or view freinds profile (f):"))
    if profile_choice == "w":
        title_profile(username, profile)

    elif profile_choice == "c":
        selection = str(input("Enter section you want to continue from or append/change (title, major, university, about section, experiene, education): "))
        if "title" in selection:
            title_profile(username, profile)
        elif "major" in selection:
            major_profile(username, profile)
        elif "university" in selection:
            university_profile(username, profile)
        elif "about section" in selection:
            about_profile(username, profile)
        elif "experience" in selection:
            experiences_profile(username, profile)
        elif "education" in selection:
            education_profile(username, profile)
        else:
            print("invalid input")
            create_profile(account, username, profile)

    elif profile_choice == "v":
        view_profile(account,username, profile)

    elif profile_choice == "f":
        view_friend_profile(account, username, profile)

def title_profile(username, profile):
    title = str(input("Enter profile title:"))
    text_file = open("text_file.txt", "w")
    text_file.write(title)
    whole_file = text_file.readlines()
    text_file.close()
    if len(whole_file) > 1:
        print("Maximum 1 line of text.\n")
        title_profile(username, profile)

    profile[username]["title"]=title
    with open('profile.json', 'w') as file:
        file.write(json.dumps(profile))
    cont = str(input("Do you wish to continue to the next section (Y) or save it for later (N)?"))
    if cont == ("Y" or "y"):
        major_profile(username, profile)
    else:
        return()
        
def major_profile(username, profile):
    major = str(input("Enter your major:"))
    profile[username]["Major"]=major
    with open('profile.json', 'w') as file:
        file.write(json.dumps(profile))
    cont = str(input("Do you wish to continue to the next section (Y) or save it for later (N)?"))
    if cont == ("Y" or "y"):
        university_profile(username, profile)
    else:
        return()
    
def university_profile(username, profile):
    university_name = str(input("Enter University name:"))
    profile[username]["University"]= university_name
    with open('profile.json', 'w') as file:
        file.write(json.dumps(profile))
    cont = str(input("Do you wish to continue to the next section (Y) or save it for later (N)?"))
    if cont == ("Y" or "y"):
        about_profile(username, profile)
    else:
        return()
    
def about_profile(username, profile):
    about = str(input("Insert information about yourself:"))
    profile[username]["information"]= about
    with open('profile.json', 'w') as file:
        file.write(json.dumps(profile))
    cont = str(input("Do you wish to continue to the next section (Y) or save it for later (N)?"))
    if cont == ("Y" or "y"):
        experiences_profile(username, profile)
    else:
        return()
    
def experiences_profile(username, profile):
    num_experience = int(input("Number of experiences you want to enter:"))
    i=0
    while i < num_experience:
        i+=1
        title = str(input("Title: "))
        employer = str(input("Employer Name: "))
        date_start = str(input("Date started:"))
        date_ended = str(input("Date ended:"))
        loc = str(input("Enter Location: "))
        desc = str(input("Job Description: "))

        job = {
            "title": title,
            "employer": employer,
            "Start Date": date_start,
            "End Date": date_ended,
            "job location": loc,
            "job Description": desc
        }
        profile[username]["experience"]=job
    with open('profile.json', 'w') as file:
        file.write(json.dumps(profile))
    cont = str(input("Do you wish to continue to the next section (Y) or save it for later (N)?"))
    if cont == ("Y" or "y"):
        education_profile(username, profile)
    else:
        return()


def education_profile(username, profile):
    print("Enter education information:")
    school_name = str(input("Enter school name:"))
    degree = str(input("Enter degree:"))
    years = int(input("Enter years attended: "))

    education = {
        "School Name": school_name,
        "Degree": degree,
        "Years": years
    }
    profile[username]["education"]=education
    with open('profile.json', 'w') as file:
        file.write(json.dumps(profile))

def view_profile(accounts, username, profile):
    print(accounts.name)
    f = open('profile.json')
    data = json.load(f.read())
    print(data)
    f.close()

def view_friend_profile(accounts, username, profile):
    print("This is a list of your friends")



def search_job(account, username):
    job_title = input("Enter the title of the job/internship you're looking for: ")
    location = input("Enter the location: ")
    salary = input("Enter the expected salary (optional): ")
    for employer in account:
        if "Jobs" in account[employer]:
            for job_title in account[employer]["Jobs"]:
                job = account[employer]["Jobs"][job_title]
                apply = str(input("Do you wish to apply for this job now? Y or N"))
                if apply == ("Y" or "y"):
                    if job in account[JobPost]:
                        print("Sorry, you cannot apply for a job you posted.\n")
                        search_job(account, username)
                    if job in account[username]["Jobs Applied"]:
                        print("You have already applied for this job\n")
                        search_job(account, username)

                    else:
                        grad_date = str(input("Please enter a graduation date: (mm/dd/yyyy)"))
                        start_date = str(input("Please enter a start date: (mm/dd/yyyy)"))
                        self_description = str(input("Please explain why you would be a good fit for this job: "))
                        account[username]["Jobs Applied"].append(Job = job, Graduation = grad_date, Start = start_date, Description = self_description)
                        jobs_applied(account, username)
                
                elif apply == ("N" or "n"):
                    save = str(input("Do you want to save this job to apply for later? Y or N"))
                    if save == ("Y" or "y"):
                        account[username]["Jobs Saved"].append(job)
                    elif save == ("N" or "n"):
                        search_job(account, username)


def jobs_applied(accounts, username):
    print("List of jobs applied for:",accounts[username]["Jobs Applied"])

def jobs_saved(accounts, username):
    print("List of jobs saved",accounts[username]["Jobs Saved"])
    remove = str(input("Do you wish to remove a job from the saved list? Y or N"))
    if remove == ("Y" or "y"):
        job_removed = str(input("Insert job title you wish to remove:"))
        if job_removed in accounts[username]["Jobs Saved"]:
            accounts[username]["Jobs Saved"].remove(job_removed)



def main():
    print('''The platform of InCollege is able to convey its value proposition to potential users 
who have not yet joined up by displaying a real-life example of a student who utilized InCollege to land a job. 
This may be a powerful method to entice users to explore the platform more and create an account. 
As consumers can see that InCollege has already assisted others in accomplishing their goals, it can also serve to increase trust in the site.\n''')

    video = input(
        ("Type \"yes\" or \"no\" for a video to be displaying explaining why they would want ot join InCollege: "))
    if video == "yes":
        print("Video is now playing")

    navi_links = input(
        "Useful Links | InCollege Important Links | Languages | Profiles \n(Type U for Useful links or I for InCollege Important Links or 'L' for Languages or 'P' for Profiles : ")
    if navi_links == "U":
        useful_links()
    elif navi_links == "I":
        important_links()
    elif navi_links == "L":
        language()
    elif navi_links == "P":
        username = str(input("Enter existing username: "))
        accounts= loadFile()
        profile= loadProfile()
        creating_all_profiles(accounts, profile)
        create_profile(accounts, username, profile)
        jobs_applied(accounts, username)
        jobs_saved(accounts, username)

if __name__ == "__main__":
    main()