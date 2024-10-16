# Personal and Business Facts Assistant

This project provides a framework for storing and retrieving personal or business facts from a vector database using a Language Model (LLM) to dynamically handle queries. The assistant is capable of understanding user input and storing relevant facts with separate fact type (e.g., personal and business facts). It can later retrieve these facts based on the context of the user's queries, allowing for more personalized and context-aware responses.

## Features

- **Fact Storage:**
  - The assistant can store user-provided facts, such as personal preferences or business-related information, into vectro database without overwriting previously stored facts. Each new fact is upserted to the existing index in the relevant vector store.
  
- **Fact Retrieval:**
  - The assistant retrieves stored facts based on user queries. It uses an LLM to understand the user’s input and match it with the stored facts, even if the phrasing or language differs from the original input.

- **Multilingual Support:**
  - By leveraging the LLM's capabilities, the assistant can understand and store facts in different languages. It also retrieves relevant facts regardless of the language used in the query, making it adaptable to a multilingual environment.

- **Parallel Function Calls:**
  - The system supports parallel function calls to handle multiple tasks efficiently, such as storing facts and simultaneously retrieving others based on user requests.

- **Flexible Search:**
  - The assistant uses a semantic approach to matching user queries with stored facts, which means it doesn't rely on strict keyword matching. This allows for a more intuitive and user-friendly experience when retrieving facts.

## Use Cases

- **Personalized Responses:**
  - The assistant can recall user preferences and deliver customized content, such as generating recipes, offering recommendations, or filtering information based on stored facts.
  
- **Business Data Handling:**
  - In a business context, the assistant can store and retrieve details about products, services, or customer preferences. This feature can be used to generate relevant business insights or handle customer inquiries more efficiently.

- **Contextual Memory:**
  - The assistant retains information from previous interactions, enabling it to adapt and provide more meaningful responses in future conversations, even in unrelated sessions.

## How It Works

1. **User Input:**
   - Users provide input, such as personal preferences ("I don't like apples") or business-related facts.

2. **Fact Storage:**
   - The assistant analyzes the input and stores the extracted facts in the relevant vectorstore index (either for personal or business facts), ensuring that existing facts are not overwritten.

3. **Fact Retrieval:**
   - When a user asks a question, the assistant retrieves stored facts that match the query context. For instance, if the user requests, "Make me a recipe for a fruit salad, but without the fruit I don't like," the assistant searches for previously stored facts to exclude disliked fruits.

4. **Multilingual Queries:**
   - Users can provide input or ask queries in different languages, and the assistant will still be able to store and retrieve relevant facts, thanks to the LLM’s multilingual support.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

### MIT License

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

---
