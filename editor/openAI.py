from openai import OpenAI
import json

# os.environ['OPENAI_API_KEY'] = 
def get_coding_problem():
    # return 'Coding Problem'
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
A standard coding problem format with a title, overview, and example. Also an explanation section at the end if there is a key concept they don't already understand in the problem. Use JSON format. Don't ever ask them to use the input function in their python code.

Example Output:
{
    "name": "Palindrome  Checker",
    "overview": "This coding problem requires you to determine whether a given string is a palindrome. A palindrome is a word, phrase, number, or other sequence of characters that reads the same forward and backward (ignoring spaces, punctuation, and capitalization). Your task is to write a function that takes a string as input and returns true if it is a palindrome, and false otherwise.",
    "examples": 
             [
                {
                    "input": "A man, a plan, a canal, Panama",
                    "expected_response": "true"
                },
                {
                    "input": "Hello",
                    "expected_response": "false"
                }
             ],
    "new_concept":  
             {
                name: "Indexing a String",
                "explanation": "In order to work closely with the parts of a string, the [] syntax can be used. Just like a list, strings can be accessed by index using the square brackets. For example, my_string[0] would be the first character in my_string."
             }
}
             """},
            {
                "role": "user",
                "content": "I need a coding problem, I already understand the print statement but that's it"
            }
        ]
    )
    return json.loads(completion.choices[0].message.content)

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
                "content": f"{{problem : {problem}, code : {code_str}}}"
            }
        ]
    )
    return completion.choices[0].message.content

def get_answer(question, context):
    client = OpenAI()

    completion = client.chat.completions.create(
        model = "gpt-4o-mini",
        messages = [
            {"role": "system", "content": """
            Full Context:
You are a python instructor who gives your students coding problems. Your student is sending you a question relating to their problem. You need to answer them as concisely as possible. Do not allow them to get off topic.

Steps:
1. Compare the question to the problem they are solving and the code they have written.
2. Answer the question based on the code they have written and the problem they are trying to solve.
3. Ensure that the answer will not give away the solution to the problem unless the student is clearly struggling and needs to be given the solution.

Input Format:
A JSON object with a question and context which includes the entire conversation, as well as the problem you have sent them and their code.

Output Format:
A simple answer in string format which answers the question and perhaps includes a link to an online resource with more information.

Example Output:
The error on line 5 you are asking about is caused by indexing off the end of a list. This often happens when we forget that list's indices start at 0
             """},
            {
                "role": "user",
                "content": f"{{question : {question}, context : {context}}}"
            }
        ]
    )
    return completion.choices[0].message.content
