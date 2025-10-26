# Natural Language to SQL Experiments

In this repository, I explore and experiment with building natural language interfaces to SQL databases — systems that translate human language queries into executable SQL statements.

## Schema Aware SQL Generation

The following diagram illustrates the schema-aware generation pipeline:

![pipeline](design/schema_awareness.png)

### Context

> First, an LLM is assigned to identify the relevant tables required to handle the user’s request. It returns a list of table names to the next node, which executes a SELECT statement to fetch the first row from each table along with their schemas. This information is then prepared and passed to the SQL generation agent.

#### Nodes Response

```txt
Table: `departments`

Schema: [{'name': 'department_id', 'type': 'INTEGER', 'notnull': False, 'is_primary_key': True}, {'name': 'name', 'type': 'TEXT', 'notnull': True, 'is_primary_key': False}]

Sample Rows (Columns: ['department_id', 'name']):
[{'department_id': 1, 'name': 'Computer Science'}, {'department_id': 2, 'name': 'Mathematics'}, {'department_id': 3, 'name': 'History'}]

---

Table: `students`

Schema: [{'name': 'student_id', 'type': 'INTEGER', 'notnull': False, 'is_primary_key': True}, {'name': 'name', 'type': 'TEXT', 'notnull': True, 'is_primary_key': False}, {'name': 'department_id', 'type': 'INTEGER', 'notnull': False, 'is_primary_key': False}]

Foreign Keys: [{'from_column': 'department_id', 'to_table': 'departments', 'to_column': 'department_id'}]

Sample Rows (Columns: ['student_id', 'name', 'department_id']):
[{'student_id': 1, 'name': 'John Doe', 'department_id': 1}, {'student_id': 2, 'name': 'Jane Roe', 'department_id': 2}, {'student_id': 3, 'name': 'Mark Spencer', 'department_id': 1}]
```

### SQL Generation

> The LLM takes the user’s question along with the relevant schema context to generate an SQL query. Another node then executes the query on the database and handles the retry mechanism.

#### SQL Generation & Retry Mechanism

![pipeline](design/sql_gen.png)

- The LLM generates the SQL statement based on the input query and schema context.
- The execution node ensures security by blocking harmful or unsafe queries and manages error handling and retry mechanisms.

### Natural Language Response

> Given user question and SQL results to generate a readable response for the user.

### Technologies

`Gemini-SDK` `LangGraph` `Pydantic` `SQLight` `FastAPI` `Uvicorn`

---

## Modeling

### Gemma3 Text-to-SQL Fine-Tuning with QLoRA

Fine-tuning the google/gemma-3-1b-pt model on a Text-to-SQL task. The training script uses the Hugging Face trl library to perform supervised fine-tuning (SFT) with PEFT (QLoRA) for memory-efficient training.

- Tokenizer: `google/gemma-3-1b-it` (the instruction-tuned tokenizer)
- Dataset: `philschmid/gretel-synthetic-text-to-sql`
- Technologies: Hugging Face `transformers`, `datasets`, `peft`, and `trl`
- Techniques: 4-bit Quantization (QLoRA) via `bitsandbytes`

### Workflow

1. Dataset: Loads the *philschmid/gretel-synthetic-text-to-sql* dataset from the Hugging Face Hub.
2. Formatting: A custom prompt template is defined to structure the SQL context and the user's question. The dataset is then mapped to this chat format:
      - System Message: Instructions to be an SQL assistant.
      - User: Contains the prompt template with the {context} (schema) and {question} (natural language query).
      - Assistant: Contains the target {sql} query.
3. Sampling: For demonstration purposes, the script shuffles the dataset, selects 80 samples, and then creates an 80/20 train/test split.
4. Model Loading:
      - Loads the google/gemma-3-1b-pt model.
      - Applies 4-bit quantization to reduce memory usage significantly.
      - Sets the appropriate torch_dtype (bfloat16 or float16) based on your GPU capability.
5. Tokenizer: Loads the google/gemma-3-1b-it (Instruction) tokenizer to correctly apply the Gemma chat template.
6. PEFT (QLoRA) Config:
      - Sets up LoraConfig to inject adapters into all linear layers.
      - Saves the lm_head and embed_tokens to ensure they are trained along with the new adapters.
7. Training Arguments:
      - Configures SFTConfig with key parameters like max_seq_length, packing=True (for efficiency), per_device_train_batch_size, and QLoRA-specific settings (learning_rate, max_grad_norm, etc.).
8. Trainer Initialization: Initializes an SFTTrainer object, making it ready for training.
