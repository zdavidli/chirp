# Iteration 3 Evaluation - Group 18

**Evaluator: [Srini Suresh](mailto:ssures11@jhu.edu)**

### Implementation progress
Saw a very very basic demo during the lab and it was alright. But in the coming weeks I want to see this feature you have up work end to end.

### Design check-in
Yes I see that you've checked in an Android component to read texts. I'm not sure how far along you are though, as you have a god-activity that does more than login.

Don't re-invent the wheel. Use a library for something that is not core to your app. Like [this](https://github.com/CodelightStudios/Android-Smart-Login) to complete the login flows.

### Code Quality
I understand that you are still getting things started. But a lot of your Java code follows a god class anti pattern. FYI, when copying code from StackOverflow verbatim (this itself is fine btw) you are supposed to credit the answer with a link. If you change the code then this is not required.

Document your code as you go along, eg: Javadoc, pydoc etc.

Your Python code is not very object oriented. Also, Please get rid of the .pyc files. Not dinging you now, but please fix.

### Git usage
I've told you in the lab as well, delete the named branch. Other than CMUdict you have no feature level branches.
I don't see many checkins from Richard **-2**

#### Use of the GitHub issue tracker to manage bugs, features, etc.
You have only 2 issues one of which I opened. **-2**

#### Codebase pushed to master on your team's GitHub repository for our inspection
Taking into account that you write only to master, yes.

### Iteration submission and reporting
You still haven't fixed your API spec. Dinging you harder to get your attention **-20**

#### Fully automated build of your project with a README.md describing how to build it
build.sh appears to succeed. Which is weird because I don't even have the Android dev tools on my system.
Also your build.sh right now only calls gradlew with build in bash. When I try this from within the Android folder build fails. This is not right **-5**

#### Top-level file CHANGELOG.md present in your repo and describes progress in this iteration well
Passable.

#### Use of GitHub's project boards to keep track of your progress
You have some boards. But only 1 is in use. The tasks are not moved along to iteration 4. You have to label and use the boards more meticulously.

### Other Remarks
You lost points that could have easily been saved. Please fix the highlighted issues.


**Grade: 71/100**
