from app.pipeline.llm_instance import llm

def llm_meaningful_change_detect(old_sentence: str, new_sentence: str) -> bool:
    prompt = f"""[INST] <<SYS>>
    You are a helpful assistant focused on analyzing changes in privacy policies. Answer with one word only.
    <</SYS>>
    OLD: {old_sentence}
    NEW: {new_sentence}

    Is this a meaningful change that affects user privacy? Answer with one word: yes or no.
    [/INST]"""  
    

    output = llm(prompt, max_tokens=10)
    response = output["choices"][0]["text"].strip().lower()
    # print("***************LLM Analysis:")
    # print("old: " + old_sentence)
    # print("new: " + new_sentence)
    # print(f"LLM Response: {response}")  # Debugging output
    # print("***************")
    return "yes" in response



def batch_llm_meaningful_change_detect(pairs, batch_size=10):
    all_results = []
    
    for i in range(0, len(pairs), batch_size):
        batch = pairs[i:i+batch_size]
        
        # Shared system instruction only once
        prompt = "[INST] <<SYS>>\nYou are an assistant helping to detect **meaningful changes** in privacy policies. A meaningful change is one that affects **user privacy, data collection, sharing, retention, or user rights**. For each pair of sentences (old vs. new), answer **only 'yes' or 'no'**: - 'Yes' if the change has **privacy implications** or alters **user control/data practices**. - 'No' if the change is **stylistic**, **grammatical**, or **does not affect user data**. \n<</SYS>>\n"

        for old, new in batch:
            prompt += f"OLD: {old}\nNEW: {new}\nIs this a meaningful change that affects user privacy? Answer yes or no.\n\n"
        
        prompt += "[/INST]"
        
        output = llm(prompt, max_tokens=10 * len(batch))
        text = output["choices"][0]["text"].strip().lower()
        print("@@@@@@@@@TEXT@@@@@@@@@@")
        print(text)
        print("@@@@@@@@@@@@@@@@@@@")
        
        # Split by line, filtering out garbage
        answers = [line.strip() for line in text.splitlines() if line.strip() in ("yes", "no")]
        print("@@@@@@@@@ANSWERS@@@@@@@@@@")
        print(answers)
        print("@@@@@@@@@@@@@@@@@@@")
        results = ["yes" in a for a in answers]
        
        all_results.extend(results)
    
    print("@@@@@@@@@ALL RESULTS@@@@@@@@@@")
    print(all_results )
    print("@@@@@@@@@ALL RESULTS@@@@@@@@@@")
    return all_results

