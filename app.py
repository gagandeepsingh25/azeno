from flask import Flask, request, render_template, jsonify,session
import openai
from openai import OpenAI
import os
import time
from main_calculations import *
app = Flask(__name__)
app.secret_key = "hello"

# api_key =  os.environ["OPENAI_API_KEY"] = "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"
api_key = os.environ["OPENAI_API_KEY"] = "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"


# client = openai.OpenAI(api_key = "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")
@app.route('/')
def home():
    print("????????????")
    session["response"] = None
    return render_template('chatbot1.html')  # Ensure you have an index.html file in a templates directory


@app.route('/ask', methods=['POST'])
def ask():

    user_input = request.form.get('user_input')
    print(user_input, "user_input")
    # global response,user_input
    print("Route /ask has been hit.")
    # chattype = "Productselection"
    if "response" in session:
        response = session["response"]

    print(response, "----------------response-------------")
    if response is None:
        user_input = request.form.get('user_input', 'No input received')
        print(f"User Input: {user_input}")
        session["productselection"] = user_input

        response_message = "Please enter the size of the configuration (Width x Length in feet) \nAlways list Width First! (e.g., 15'x13')"
        session["response"] = response_message
    else:
        if response.__contains__("enter the size"):
            size = user_input
            session["size"] = user_input
            selected_product = session["productselection"]
            bays, bay_width, bay_length, price = main_price_cal(selected_product=selected_product, size=size)
            response_message=f'Number of Bays based on the dimensions: {bays} \n Widt                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     h of single Bay based on the dimensions: {bay_width}\n Price based on Width dimensions:{price} \n\n\nWhat type of structure is needed? \n1. Freestanding \n2. Attached 1 Si\n3. Footings'
            session["response"] = response_message
            session['bays'] = bays
            session['bay_width'] = bay_width
            session['bay_length'] = bay_length
            session['price'] = price

        if response.__contains__("type of structure"):
            user_input = request.form.get('user_input', 'No input received')
            print(f"User Input: {user_input}")
            session["structureselection"] = user_input
            bays = session['bays']
            bay_width = session['bay_width']
            bay_length = session['bay_length']
            price = session['price']
            size = session['size']

            if "structureselection" in session:
                structureselection = session["structureselection"]

            print(structureselection, "----------------structureselection------", type(structureselection))
            # if session["structureselection"]==1:
            #     structure_type = "1"
            #     print("yesssssssssssssssssssss")
            # if session["structureselection"]==2:
            #     structure_type = "2"
            # if session["structureselection"]==3:
            #     structure_type = '3'
            #
            if structureselection == "1":
                structure_type = "1"
                posts, post_bases, postsCost, post_basesCost, total_post_cost, sensorP, b2b, p2g, bensorP_cost, R2b_cost, p2g_cost, remote_control = postCostCal(
                    structure_type=structure_type, size=size, bays=bays)

                response_message = f"Number of posts required: {posts}\n\nNumber of posts caps required: {post_bases} \nTotal cost: {posts} * 1500 + {post_bases} * 275 = {postsCost}\nsensorP:{sensorP}\nb2b:{b2b}\np2g:{p2g}\n b2b_cost:{b2b_cost}\n p2g_cost:{p2g_cost}\n sensorP_cost:{sensorP_cost}\n Remote_control:{Remote_control}"
                # session["response"] = response_message

            if structureselection == "2":
                structure_type = "2"
                posts, post_bases, postsCost, post_basesCost, total_post_cost, sensorP, b2b, p2g, b2b_cost, p2g_cost, sensorP_cost, Remote_control = postCostCal(
                    structure_type=structure_type, size=size, bays=bays)

                response_message = f"Number of posts required: {posts}\n\nNumber of posts caps required: {post_bases} \nTotal cost: {posts} * 1500 + {post_bases} * 275 = {postsCost}\nsensorP:{sensorP}\nb2b:{b2b}\np2g:{p2g}\n b2b_cost:{b2b_cost}\n p2g_cost:{p2g_cost}\n sensorP_cost:{sensorP_cost}\n Remote_control:{Remote_control}"
                # session["response"] = response_message

            if structureselection == "3":
                posts, post_bases, postsCost, post_basesCost, total_post_cost, sensorP, b2b, p2g, b2b_cost, p2g_cost, sensorP_cost, Remote_control = postCostCal(
                    structure_type=structure_type, size=size, bays=bays)

                response_message = f"Number of footings required: {posts}\n\nTotal cost: {posts} * 600 = {postsCost}\nnsensorP:{sensorP}\nb2b:{b2b}\np2g:{p2g}\n b2b_cost:{b2b_cost}\n p2g_cost:{p2g_cost}\n sensorP_cost:{sensorP_cost}\n Remote_control:{Remote_control}"
                # session["response"] = response_message

                structure_type = '3'
            response_message += '\n\n\nSelect material type \n1. Corbels\n2. Single Cornice\n3. Double Cornice'
            session["response"] = response_message

            # design_type = "Corbels"

        if response.__contains__("footings required"):
            size = session['size']
            user_input = request.form.get('user_input', 'No input received')
            print(f"User Input: {user_input}")
            session["structureselection"] = user_input
            if user_input == "1":
                design_type = "Corbels"
            if user_input == "2":
                design_type = "Single Cornice"
            if user_input == "3":
                design_type = "Double Cornice"

            installation_cost, shipping_cost, Total_design_cost = installationCost(size=size, design_type=design_type)

            # Additional accessories:


            final_cost = price + total_post_cost + b2b_cost + p2g_cost + sensorP_cost + installation_cost + shipping_cost + Remote_control + Total_design_cost

            print("\nFinal Total Cost:")
            print(f"Total Bays Price: {price}")
            print(f"Posts/Footings and Caps Cost: {total_post_cost}")
            print(f"Beam to Beam Cost: {b2b_cost}")
            print(f"Pass Through Gutter Cost: {p2g_cost}")
            print(f"Sensor Package Cost: {sensorP_cost}")
            print(f"Installation Cost: {installation_cost}")
            print(f"Shipping Cost: {shipping_cost}")
            print(f"Remote Control Cost: {Remote_control}")
            print(f"Total Design Cost: {Total_design_cost}")
            print(f"\nFINAL COST: {final_cost}")
            # print(final_cost)

            response_message = f"Total Bays Price: {price}\n" \
                               f"Posts/Footings and Caps Cost: {total_post_cost}\n" \
                               f"Beam to Beam Cost: {b2b_cost}\n" \
                               f"Pass Through Gutter Cost: {p2g_cost}\n" \
                               f"Sensor Package Cost: {sensorP_cost}\n" \
                               f"Installation Cost: {installation_cost}\n" \
                               f"Shipping Cost: {shipping_cost}\n" \
                               f"Remote Control Cost: {Remote_control}\n" \
                               f"Total Design Cost: {Total_design_cost}\n" \
                               f"FINAL COST: {final_cost}"

        if response.__contains__("Additional accessories"):
            user_input = request.form.get('user_input', 'No input received')
            print(f"User Input for Customization: {user_input}")
            session["customization"] = user_input
            if user_input == "1":
                accessory = "Recessed Lights"
                # ask for quantity
            if user_input == "2":
                accessory = "Ramp Lights"
                # ask for quantity
            if user_input == "3":
                accessory = "Strip Light Control Box"
                # ask for quantity
            if user_input == "4":
                accessory = "LED Strip Lights"
                # ask for length in foot
            if user_input == "5":
                accessory = "Ramp Lights"



    # # if "size" in session:
    # #     size = session["size"]
    # # selected_product = "1"
    # # size = "14 x 16"
    # structure_type = 'Freestanding'
    # design_type = "Corbels"
    #
    # bays, bay_width, bay_length, price = main_price_cal(selected_product=selected_product, size=size)
    # posts, post_bases, postsCost, post_basesCost, total_post_cost, sensorP, b2b, p2g, b2b_cost, p2g_cost, sensorP_cost, Remote_control = postCostCal(
    #     structure_type=structure_type, size=size,bays=bays)
    # intallation_cost, shipping_cost, Total_design_cost = installationCost(size=size, design_type=design_type)
    # #
    # final_cost = price + total_post_cost + b2b_cost + p2g_cost + sensorP_cost + intallation_cost + shipping_cost + Remote_control + Total_design_cost
    # print(final_cost)
    #
    # response_message = final_cost

    # def greet_user():
    #     print("Welcome to the Azenco Sales Quote Generation ChatBot!")
    #     print("Please select a product from the list below:")
    #     products = ["1. R-Blade", "2. R-Shade", "3. Privacy Walls"]
    #     for product in products:
    #         print(product)
    #     selected_product = input("Enter the number of the product you'd like to select: ")
    #     return selected_product

    # response_message = main_ff(selected_product, size, structure_type, design_type)
    # # print(response_message, "response_message----------------")
    # response_message = response_message.replace("<", '&lt;')
    # response_message = response_message.replace(">", '&gt;')
    # response_message = response_message.replace("```solidity",
    #                                             '</p><code class="strict-paragraph" style="color:#252a6f;"><h5>solidity</h5>')
    # response_message = response_message.replace("```html",
    #                                             '</p><code class="strict-paragraph" style="color:#252a6f;"><h5>html</h5>')
    # response_message = response_message.replace("```python",
    #                                             '</p><code class="strict-paragraph" style="color:#252a6f;"><h5>python</h5>')
    # response_message = response_message.replace("```java",
    #                                             '</p><code class="strict-paragraph" style="color:#252a6f;"><h5>java</h5>')
    # response_message = response_message.replace("```php",
    #                                             '</p><code class="strict-paragraph" style="color:#252a6f;"><h5>php</h5>')
    # response_message = response_message.replace("```css",
    #                                             '</p><code class="strict-paragraph" style="color:#252a6f;"><h5>css</h5>')
    # response_message = response_message.replace("```c",
    #                                             '</p><code class="strict-paragraph" style="color:#252a6f;"><h5>code</h5>')
    # response_message = response_message.replace("```bash",
    #                                             '</p><code class="strict-paragraph" style="color:#252a6f;"><h5>bash</h5>')
    # response_message = response_message.replace("```", '</code><p class="strict-paragraph">')
    # #
    # response_message = response_message.replace(". ", '\n')
    # # print(response_message,'================>>>>')
    # # Split the input text into parts: introduction, Solidity code, and explanation
    # # parts = response_message.split('</code><p class="strict-paragraph">')
    # # intro_and_code = parts[0].split('</p><code class="strict-paragraph" style="color:#252a6f;"><h5>solidity</h5>')
    # # introduction = intro_and_code[0].strip()
    # # code = intro_and_code[1].strip()
    # # explanation = parts[1].strip()
    # #
    # # # Clean up the Solidity code (remove HTML entities and correct ">" conversion)
    # # code_cleaned = code.replace("&gt;", ">")
    # #
    # # # Split the Solidity code into lines for proper indentation
    # # code_lines = code_cleaned.split(";")
    # # formatted_code = ";\n".join(code_lines).strip(';')
    # #
    # # # Assemble the formatted text
    # # formatted_text = f"{introduction}\n\nSolidity Code:\n{formatted_code}\n\nExplanation:\n{explanation}"
    #
    # # print(formatted_text)

    return jsonify({"message": str(response_message)})


def create_thread_and_run(user_input):
    # Initialize the OpenAI client
    client = OpenAI()

    def validate_response(response):
        # print(response,'========')
        """Check if the response contains any of the keywords related to the domain."""
        keywords = ["XinFin", "eXchange inFinite", "hybrid blockchain", "global trade", "finance", "public blockchains",
                    "private blockchains", "scalable", "secure", "efficient", "XDC protocol",
                    "public state verification", "enterprise operations", "XDC Token", "transactions",
                    "computational services", "EVM Compatibility", "Ethereum Virtual Machine", "smart contracts",
                    "DApps", "Consensus Mechanism", "XinFin Delegated Proof of Stake", "XDPoS", "democratic governance",
                    "transaction validation", "High Transaction Speed", "block time", "Energy Efficient"]
        content = response.content
        responsee = content
        # print(responsee, '----')
        return any(keyword in responsee for keyword in keywords)

    # Assistant and user prompts
    gpt_system_prompt = ("This GPT specializes only in generating software code across various languages with a "
                         "particular"
                         "emphasis on smart contract development for the XinFin XDC Network. It aids"
                         "users in designing applications optimized for the XDC Network's unique features and "
                         "requirements, such as its consensus mechanism, EVM compatibility, and transaction speed. "
                         "The GPT provides guidance on best practices for developing on the XinFin Network, "
                         "including security considerations, gas optimization, and integration with XDC. You "
                         "specialize in smart contract development for the XinFin XDC Network. Please ask me "
                         "anything related to this domain. For questions outside this area, you recommend "
                         "consulting a relevant expert or resource.")
    gpt_user_prompt = user_input
    message = [{"role": "system", "content": gpt_system_prompt}, {"role": "user", "content": gpt_user_prompt}]

    # API request parameters
    temperature = 0
    max_tokens = 8000
    frequency_penalty = 0.0

    # Generate and validate the response
    # Assuming the rest of the generate_and_validate_gpt_response function remains the same...

    # def generate_and_validate_gpt_response(message, temperature, max_tokens, frequency_penalty):
    """Generate a GPT response and validate its relevance."""
    response = client.chat.completions.create(
        model="gpt-4",
        messages=message,
        temperature=temperature,
        max_tokens=max_tokens,
        frequency_penalty=frequency_penalty
    )
    response_text = response.choices[0].message

    # Debugging: Print the actual response to see why validation might fail
    # print("GPT Response:", response_text)  # Debugging line to see the response
    print(response_text, '*(((((9999999999999999999999999999999999999')
    content = response_text.content
    responsee = content
    print("MyGpt Response:", responsee)
    # # Validate the response
    # if validate_response(response_text):
    #     content = response_text.content
    #     responsee = content
    #     print("MyGpt Response:", responsee)
    # else:
    #     responsee = ('Please consult a relevant expert or resource.Or you can refine your query to focus more on the XinFin XDC Network and smart '
    #                  'contract development')

    return responsee


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000, threaded=False)

#     # Initialize the client
#     client = openai.OpenAI()
#     a_list = client.beta.assistants.list()
#     assitant_obj_list = a_list.data
#     for i in range(len(assitant_obj_list)):
#         if assitant_obj_list[i].name == "Draft Letter Of Offer Assistant":
#             os.environ["assistant_id"] = assitant_obj_list[i].id
#             break
#         else:
#             pass
#         # print(assitant_obj_list[i].name)
#         # client.beta.assistants.delete(assitant_obj_list[i].id)
#
#     file = client.files.create(file=open("dlof.pdf", "rb"), purpose='assistants')
#
#     #  Create an Assistant (Note model="gpt-3.5-turbo-1106" instead of "gpt-4-1106-preview")
#     try:
#         print('Assistant Already exist.')
#         assistant = client.beta.assistants.retrieve(os.environ["assistant_id"])
#     except:
#         assistant = client.beta.assistants.create(
#             name="Draft Letter Of Offer Assistant",
#             instructions="You are a merger and takeover specialist chatbot. Use your knowledge base to best respond to queries related to mergers and takeovers. Pls be precise",
#             model="gpt-3.5-turbo-1106",
#             tools=[{"type": "retrieval"}],
#             file_ids=[file.id]
#         )
#
#     #  Create a Thread
#     thread = client.beta.threads.create()
#
#     # Add a Message to a Thread
#     message = client.beta.threads.messages.create(thread_id=thread.id, role="user",
#                                                   content=user_input
#                                                   )
#
#     # Run the Assistant
#     run = client.beta.threads.runs.create(thread_id=thread.id, assistant_id=assistant.id,
#                                           instructions="Please address the user as MnA User")
#     print(run.model_dump_json(indent=4))
#
#     # If run is 'completed', get messages and print
#     while True:
#         # Retrieve the run status
#         run_status = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
#         # print(run_status.model_dump_json(indent=4),"ssssss")
#         time.sleep(2)
#         if run_status.status == 'completed':
#             messages = client.beta.threads.messages.list(thread_id=thread.id)
#             textmessages = messages.data[0].content[0].text
#             print(textmessages, ">>>>>>>>>>>>>>>>>>>.")
#             return textmessages
#         else:
#             ### sleep again
#             time.sleep(2)
