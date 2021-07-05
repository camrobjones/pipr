// Item types
const PASSIVE   = "PASSIVE";
const ACTIVE    = "ACTIVE";
const FILLER    = "FILLER";
const PRAC      = "PRAC";

// experimental, filler and practice items from:
// Caterina Laura Paolazzi, Nino Grillo, Artemis Alexiadou & Andrea Santi (2019)
// Passives are not hard to interpret but hard to remember: evidence from
// online and offline studies, Language, Cognition and Neuroscience,
// 34:8, 991-1015, DOI: 10.1080/23273798.2019.1602733.
// Questions made up by Iris Mulders.

// Lists 
const LISTS = [
    "list1",
    "list2"
    // "list3"
];

const PRACTICE_ITEMS = [
    {
        id : 1,
        item_type : PRAC,

        stimulus :                                                // Single "/" delimit boundaries between words presented
                                                                  // together. Boundaries must be activated by setting "/" as
                                                                  // GROUPING_STRING in globals.js. The default is null
                                                                  // which means every word is a group of in its own.
                                                                  // If the grouping string isn't set or null,
                                                                  // the "/" will be displayed instead of used for grouping.
                                                                  // The '+' adds strings together or concatenates them.
                                                                  // A "\n" makes the string jump to the next line.
                                                                  // use a comma here.

            "Neil was /about to /go into /a job interview. /He was generally \n" +
            "/satisfied in /his current job /but he thought /that he deserved \n" +
            "/to be paid /more money. /The hiring manager /invited Neil \n" +
            "/into his office /and asked him /to take /a seat. /He asked Neil \n" +
            "/several difficult /questions about /technical aspects /of the job. \n" +
            "/The hiring manager /admired Neil /because he was /so confident \n" +
            "/and eloquent. /The interview /lasted around /half an hour. \n" +
            "/At the end, /Neil got up /and thanked /the manager \n" +
            "/for the opportunity. /He felt that / the interview /had gone well.",

            
        question : "",                                            // An empty string means no question for this trial.
        qanswer : undefined                                     // We can't define a answer if there ain't no question.
    },
    {
        id : 2,
        item_type : PRAC,
        stimulus :
            "Beth was trying /to make /a ropeswing. /She was out /in a small \n" +
            "/forest near /her house /and she /had identified /the ideal tree: \n" +
            "/it had /a strong /horizontal branch /which came /up to about \n" +
            "/her head height. /She had brought /with her /a long piece /of rope. \n" +
            "/However, /when Beth tied /the rope around /the branch /and tried \n" +
            "/to go /for a swing, /it snapped! /She tumbled /to the ground \n" +
            "/in a heap. /She still /had a lot /of rope left, /so she tied \n" +
            "/another bit /of rope /to the same /branch and /tried again.",
        question: "The tree was in Beth's garden",
        qanswer : FALSE_BUTTON_TEXT
    }
];

/*
 * In this list there is a stimulus, if a word or group of words starts with a
 * '#' it's reaction time will be recorded. So don't put any '#" elsewhere...
 */
const LIST_GROUP1 = [
    {
        id : 1,
        item_type : ACTIVE,
        stimulus :
            'John was shopping /for antiques. /He was trying /to decide between \n/a beautiful /hand-blown /glass plate /and an /intricately decorated \n/steel plate. /John leaned forward /to examine /the plates \n/on the shelf. /He briefly lost /his balance /and knocked \n/into the shelf /which caused /the plates /to fall /to the floor. /When \n/#the steel plate /#fell on /#the glass plate , /#it broke. \n/#John felt terrible /#and the /store attendant /came rushing /over to \n/see what /#had happened. /#Thankfully, /#steel plate \n/#was completely unharmed /#on the floor. /#John apologised \n/profusely and /promised to pay /for the damage. ',
        question : "John was shopping for antiques.",
        qanswer : TRUE_BUTTON_TEXT
    },

    {
        id : 2,
        item_type : ACTIVE,
        stimulus :
            'Alice had spent /several years /working in Japan, /and during \n/that time /she had begun /collecting ornate swords. /One day, \n/she was showing /the collection /to her friend, /Erin. /They each \n/picked up one /of the swords: /Alice’s was /made of steel \n/while Erin’s was /made of glass. /They hit /the swords /together in \n/mock combat. /When /#the steel sword /#collided with \n/#the glass sword, /#it broke. /#Erin looked mortified /#about what \n/had happened. /Alice simply laughed /#and said /#“At least \n/#the glass sword /#is okay /#after #that clash!” /Erin was \n/very grateful /to have /such a /carefree and /supportive friend. ',
        question : "John was shopping for antiques.",
        qanswer : TRUE_BUTTON_TEXT
    },
    {
        id : 3,
        item_type : ACTIVE,
        stimulus: 'Tyler was /playing baseball /for his /High School team. /His team \n/was in /the lead, /but only by /a small margin. /It was /Tyler’s turn \n/to bat /and he /could feel /the pressure mounting. /He walked up \n/to the plate /and rested /his bat /on his shoulder. /The pitcher \n/hurled the ball. /Tyler concentrated hard, /tensed his muscles, \n/and swung confidently. /When the baseball /collided with /the bat, \n/it broke /in two. /Tyler was shocked /and took /several seconds \n/to process /what had happened. /He looked over /to see that \n/the baseball /was still /in one piece /after the collision. \n/The umpire /called for /play to stop, /while Tyler’s coach /ran over \n/to check if /he was okay. ',
        question : "John was shopping for antiques.",
        qanswer : TRUE_BUTTON_TEXT
    },
    // {
    //     id : 2,
    //     item_type : ACTIVE,
    //     stimulus :
    //         "#John was shopping /#for antiques. /#He was trying \n" +
    //         "/#to decide between /#a beautiful/ #hand-blown \n" +
    //         "/#glass plate and /#an intricately decorated \n" +
    //         "/#steel plate. /#John leaned forward /to examine \n" +
    //         "/the plates /on the shelf./ He briefly lost \n" +
    //         "/his balance and /knocked into /the shelf \n" +
    //         "/which caused /the plates /to fall /to the floor. \n" +
    //         "/#When the steel plate /#fell on /#the glass plate, \n" +
    //         "/#it broke. /The store attendant /came rushing over, \n" +
    //         "/shouting at John /for being so careless. /Thankfully, \n" +
    //         "/the glass plate /was completely unharmed /on the floor. \n" +
    //         "/John apologised profusely /and promised /to pay for \n" +
    //         "/the damage.",
    //     question : "John was shopping for antiques.",
    //     qanswer : TRUE_BUTTON_TEXT
    // },
    // {
    //     id : 3,
    //     item_type : ACTIVE,
    //     stimulus :
    //         "Intro: Alice had spent several years working in Japan, and during that time had begun collecting ornate swords. One day, she was showing the collection to her friend, Erin. They each picked up one of the swords: Alice’s was made of steel while Erin’s was made of glass. They hit the swords together in mock combat.When the steel sword collided with the glass sword, it broke. Erin looked mortified about what had happened. Alice simply laughed and said “At least the steel sword is okay after that clash!” Erin was very grateful to have such a carefree and supportive friend.",
    //     question : "John was shopping for antiques.",
    //     qanswer : TRUE_BUTTON_TEXT
    // }
    
];

/*
 * In this list there is a stimulus, if a word starts with a '#' its
 * reaction time will be recorded. So don't put any '#" elsewhere...
 */
const LIST_GROUP2 = [
    {
        id : 1,
        item_type : ACTIVE,
        stimulus :
            "The guitarist rejected #the #attractive #and\n"            +
            "#talented #singer #in #the #concert #hall #next #to\n"     +
            "#the #Irish #pub.\n"                                       ,
        question : "The singer was attractive.",
        qanswer : TRUE_BUTTON_TEXT
    },
    {
        id : 2,
        item_type : PASSIVE,
        stimulus :
            "The sculptor was mugged by #the #strange #and\n"           +
            "#temperamental #photographer #in #the #art #gallery\n"     +
            "#next #to #the #book #shop.\n"                             ,
        question : "",
        qanswer : undefined
    },
    {
        id : 3,
        item_type : FILLER,
        stimulus :
            "The beautiful princess married her young and\n"            +
            "handsome chauffeur and shocked the royal\n"                +
            "family and the press.\n"                                   ,
        question : "The chauffeur was an old man.",
        qanswer : FALSE_BUTTON_TEXT
    },
    {
        id : 4,
        item_type : FILLER,
        stimulus :
            "The little girl did not play with her brother\n"           +
            "in the colourful playground next to their weedy\n"         +
            "garden.\n"                                                 ,
        question : "",
        qanswer : undefined
    }
];

// Add a third list of stimuli when required.
// const LIST_GROUP3 = [
// ...
// ]

// These lists are not a between subjects variable, but
// define which list a participant gets.
const TEST_ITEMS = [
    {list_name: LISTS[0], table: LIST_GROUP1},
    {list_name: LISTS[1], table: LIST_GROUP2}
    // Add a third list here, put a comma on the
    // end of the line above here.
    // {list_name: LISTS[1], table: LIST_GROUP3}
];

/**
 * Get the list of practice items
 *
 * Returns an object with a list and a table, the list will always indicate
 * "practice" since it are the practice items
 *
 * @returns {object} object with list_name and table fields
 */
function getPracticeItems() {
    return {list_name : "practice", table : PRACTICE_ITEMS};
}

/**
 * This function will pick a random list from the TEST_ITEMS array.
 *
 * Returns an object with a list and a table, the list will always indicate
 * which list has been chosen for the participant.
 *
 * @returns {object} object with list_name and table fields
 */
function pickRandomList() {
    let range = function (n) {
        let empty_array = [];
        let i;
        for (i = 0; i < n; i++) {
            empty_array.push(i);
        }
        return empty_array;
    }
    let num_lists = TEST_ITEMS.length;
    var shuffled_range = jsPsych.randomization.repeat(range(num_lists), 1)
    var retlist = TEST_ITEMS[shuffled_range[0]];
    return retlist
}

