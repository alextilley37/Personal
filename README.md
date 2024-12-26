Sports Calendar Scripts

This set of scripts utilizes Google API alongside a series of sports APIs to add my favourite teams to my google calendar.

Data Sources:
Football API: Gathered by this link: https://docs.football-data.org/general/v4/team.html
Google Calendar API: https://console.cloud.google.com/apis/credentials?inv=1&invt=AblHHg&project=sports-calendar-2

Google Calendar API Notes:
Generated through Google Cloud Console:
https://console.cloud.google.com/apis/credentials?inv=1&invt=AblHHg&project=sports-calendar-2

Helpful links: 
Setting up google api: https://developers.google.com/calendar/api/quickstart/python
Example of generating calendar items: https://medium.com/@ayushbhatnagarmit/supercharge-your-scheduling-automating-google-calendar-with-python-87f752010375

Summary:
- Requires a 'Project' to be created
- Requires an Oauth credentials to be set up to be able to use your google account
- Requires API to be enabled
- Requires 'Scopes' in your Oauth to be permitted to read/write calendar items.
- Script requires a 'credentials.json' file to verify locally

To modify these, you can apply the following steps:
1. Go to the google cloud console
2. Find the Sports Calendar 2 project
3. Go to APIs & Services on the left and select "Credentials"
4. You will see Desktop client 1 - this is the Oauth client (you can download the credentials on the right)
5. To modify scopes go to OAuth consent screen, select edit app, save and continue, "add or remove scopes" (In this case we needed: ./auth/userinfo.email, ./auth/userinfo.profile, openid and ./auth/calendar)

- Once Oath is set up, the json file for the credentials was downloaded and added locally (titled credentials.json)
- The script then reads these credentials, creates a token and is then able to access the user's calendar
- The credentials may expire if not used for 6 months. You may have to follow the steps again for the 'Desktop Client 1' Oauth (in project titled Sports Calendar 2) on google cloud to set it up again
