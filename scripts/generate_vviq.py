

def generate_page(scenario, questions, i):

    page = ""

    page += f"""
<!-- Page {i} -->
<template id="vviq-{i}">

    <div>

        <h2 class='section-title likert'>
          {scenario}
        </h2>

"""

    for j_0, question in enumerate(questions):
        j = j_0 + 1

        q_text = f"""
        <!-- Question {j} -->
        <div class='question likert'>

            <h3 class='question-title likert'>{question}</h3>

            
            <div class='option-container likert'>

                <div class='radio-option likert'>

                    <label for='vviq-{i}-{j}-1' class='radio-label likert top'>
                      1
                    </label>

                    <input type='radio' name='vviq-response-{i}-{j}' id='vviq-{i}-{j}-1'
                    value="1"/ required class='likert'>

                    <label for='vviq-{i}-{j}-1' class='radio-label likert bottom'>
                      No image at all, I only “know” I am thinking of the object
                    </label>
                </div>

                <div class='radio-option likert'>

                    <label for='vviq-{i}-{j}-2' class='radio-label likert top'>
                      2
                    </label>

                    <input type='radio' name='vviq-response-{i}-{j}' id='vviq-{i}-{j}-2'
                    value="2"/ required class='likert'>

                    <label for='vviq-{i}-{j}-2' class='radio-label likert bottom'>
                      Dim and vague image
                    </label>

                </div>

                <div class='radio-option likert'>

                    <label for='vviq-{i}-{j}-3' class='radio-label likert top'>
                      3
                    </label>

                    <input type='radio' name='vviq-response-{i}-{j}' id='vviq-{i}-{j}-3'
                    value="3"/ required class='likert'>

                    <label for='vviq-{i}-{j}-3' class='radio-label likert bottom'>
                      Moderately realistic and vivid
                    </label>

                </div>

                <div class='radio-option likert'>

                    <label for='vviq-{i}-{j}-4' class='radio-label likert top'>
                      4
                    </label>

                    <input type='radio' name='vviq-response-{i}-{j}' id='vviq-{i}-{j}-4'
                    value="4"/ required class='likert'>

                    <label for='vviq-{i}-{j}-4' class='radio-label likert bottom'>
                      Realistic and reasonably vivid
                    </label>
                    
                </div>

                <div class='radio-option likert'>

                    <label for='vviq-{i}-{j}-5' class='radio-label likert top'>
                      5
                    </label>

                    <input type='radio' name='vviq-response-{i}-{j}' id='vviq-{i}-{j}-5'
                    value="5"/ required class='likert'>

                    <label for='vviq-{i}-{j}-5' class='radio-label likert bottom'>
                      Perfectly realistic, as vivid as real seeing
                    </label>

                </div>

            </div>

        </div>
        """

        page += q_text

    end = """
    </div>

</template>
    """

    page += end

    return page


vviq_data = [
    ("Think of some relative or friend whom you frequently see (but who is not with you at present) and consider carefully the picture that comes before your mind’s eye.",
        [
            "The exact contour of face, head, shoulders, and body.",
            "Characteristic poses of head, attitudes of body, etc.",
            "The precise carriage, length of step, etc. in walking.",
            "The different colors worn in some familiar clothes."
        ]),

    ("Visualize a rising sun. Consider carefully the picture that comes before your mind’s eye.",
        [
            "The sun is rising above the horizon into a hazy sky.",
            "The sky clears and surrounds the sun with blueness.",
            "Clouds. A storm blows up, with flashes of lightening.",
            "A rainbow appears."
        ]),

    ("Think of the front of a shop which you often go to. Consider the picture that comes before your mind’s eye.",
        [
            "The overall appearance of the shop from the opposite side of the road.",
            "A window display including colors, shape, and details of individual items for sale.",
            "You are near the entrance. The color, shape, and details of the door.",
            "You enter the shop and go to the counter. The counter assistant serves you. Money changes hands."
        ]),

    ("Finally, think of a country scene which involves trees, mountains, and a lake. Consider the picture that comes before your mind’s eye.",
        [
            "The contours of the landscape.",
            "The color and shape of the trees.",
            "The color and shape of the lake.",
            "A strong wind blows on the tree and on the lake causing waves."
        ])
    ]

pages = ""

for i_0, data in enumerate(vviq_data):

    i = i_0 + 1
    scenario, questions = data

    p = generate_page(scenario, questions, i)

    pages += p

with open("pipr3/data/vviq_pages.html", "w") as f:
    f.write(pages)

