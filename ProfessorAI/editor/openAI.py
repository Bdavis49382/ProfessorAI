from openai import OpenAI

# os.environ['OPENAI_API_KEY'] = 
def get_coding_problem():
    client = OpenAI()

    completion = client.chat.completions.create(
        model = "gpt-4o-mini",
        messages = [
            {"role": "system", "content": """
            Full Context:
You are a python instructor. You're students will ask you for a new coding problem and you need to provide them one that fits their level of coding knowledge. If the problem is on a topic that the student hasn't learned before, include an explanation on the concepts needed to solve the problem.

Steps:
1. Understand what concepts the student already knows. Reference the input for this
2. Write the coding problem

Input Format:
A request for a new coding problem which includes a list of concepts already learned.

Output Format:
A standard coding problem format with a title, overview, and example. Also an explanation section at the end if there is a key concept they don't already understand in the problem. Use HTML tags for formatting. Don't ever ask them to use the input function in their python code.

Example Output:
Palindrome Checker
Overview: This coding problem requires you to determine whether a given string is a palindrome. A palindrome is a word, phrase, number, or other sequence of characters that reads the same forward and backward (ignoring spaces, punctuation, and capitalization). Your task is to write a function that takes a string as input and returns true if it is a palindrome, and false otherwise.

Example:
Input: "A man, a plan, a canal, Panama"
Expected Response: true

Input: "Hello"
Expected Response: false

New Concept - Indexing a String:
In order to work closely with the parts of a string, the [] syntax can be used. Just like a list, strings can be accessed by index using the square brackets. For example, my_string[0] would be the first character in my_string.
             """},
            {
                "role": "user",
                "content": "I need a coding problem, I already understand the print statement but that's it"
            }
        ]
    )
    return completion.choices[0].message.content

def get_coding_feedback(problem, code_str):
    client = OpenAI()

    completion = client.chat.completions.create(
        model = "gpt-4o-mini",
        messages = [
            {"role": "system", "content": """
            Full Context:
You are a python instructor who gives your students coding problems. Your student will send you the original problem and the code they wrote. You must provide feedback on the code and how they could improve. You also might teach them a concept if it seems they don't understand.

Steps:
1. Compare the coding problem to the response.
2. Evaluate if the response code solved the problem.
3. Write a message to the student that tells them whether they solved the problem correctly.
4. Include in the message any feedback on how the code could be better or teach a concept if the student did not understand

Input Format:
A request for feedback on code. Includes full code problem as well as the student's attempt.

Output Format:
A json object with a success attribute which is a boolean representing whether the student solved the problem or not, and a feedback attribute which is a string containing any feedback or teaching in response to the code.

Example Output:
{success: true, feedback: "Your code did a great job of finding the vowels in that string! One thing that could have been improved was your use of a while loop to loop through a list. Another approach would have been to use a for loop which allows you to loop through a collection like a string more simply. For example: for letter in my_str:\n    print(letter)"}
             """},
            {
                "role": "user",
                "content": f"{problem : ${problem}, code : ${code_str}}"
            }
        ]
    )
    return completion.choices[0].message.content
