# jenkins_job_status

A simple tool to help follow the status on jenkins jobs

Requires a pre-created jenkins token for your user

Token can be created in the following way:
 1. In jenkins page, click the user (top right corner) and choose "Configure" from the right side menu
 2. Under "API Token", click "ADD Token", add any name for the token and click "Generate"
 3. Copy the generated string (unable to show it again later)
 4. Fill the 'user' and paste the 'token' in relevant places in 'jenkins.txt' file

To run:
1. run 'python3 setup.py'
2. Per OS:
   - On Windows machine - 'python3 main-text.py' or use the 'run.bat' batch file.
   - On Linux machine - 'python3 main-text.py'

NOTE: Only Python3.7+ has the option to use pop-up notification for finished jobs (Successful/Failed/Aborted)
