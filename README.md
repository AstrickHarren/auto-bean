# Auto bean

Write a beancount transaction with natrual language. See the following
dialogue as an example:

```
> eat out with Amy for 30.58 from cash
2023-05-11 * "" "eat out with Amy for 30.58 from cash" #share-Amy
    Expenses:Food:Dine                                         30.58 USD
    Assets:Cash                                               -30.58 USD
looks good?

> change desc eat out
2023-05-11 * "" "eat out" #share-Amy
    Expenses:Food:Dine                                         30.58 USD
    Assets:Cash                                               -30.58 USD
looks good?

> write
```

# Usage and limitation

Run the python script with your current beancount file. :warning: The script is
not fully tested, and may harm your data (although the only thing it does is
to open the file with append mode).

```bash
python cli.py <PATH TO YOUR BEAN FILE>
```

This may take several seconds on my local machine to load the language model
before the it enters the interactive mode. If it the first time, it might as
well download the AI model (see [dependencies](#dependencies)) in cache.

## Dependencies
I used [transformers](https://huggingface.co/docs/transformers) from huggingface and the [facebook model](https://huggingface.co/facebook/bart-large-mnli) for zero-shot
classification. So you may need to

1. install pytorch (or tensorflow) with pip
    ```bash
    # for torch
    python -m pip install torch
    ```
2. install transformers
    ```bash
    python -m pip install transformers
    ```

## Commands

Once in the interactive mode, here are the available commands you can use to
write a new transcation to your beancount file.

cmd | description | example
-|-|-
any other english | leave to the AI for automatic creation of a new transaction | `eat out with Amy for 30.58 paid with cash`
`change expense <Expense Type>` | change the expense type of the of the transaction, `Expense Type` can be any english, and the expense account is infered from all the accounts currently present in the beancount file| `change expense groceries`
`change from <Account>` | change the other account of the transaction (the account where the expense amount comes from) | `change from cash`
`change desc <Description>` | change the description of the transaction to exactly `Bob` | `change desc eat out`
`change payee <Payee>` | change the payee of the transcation to exactly `Payee` | `change payee Bob`
`change share <Contact>` | append a tag `#share-..` to the transaction, attempting to utilize the [beancount-share](https://github.com/Akuukis/beancount_share) plugin | `change share Amy`
`write` | append the current beancount transaction to file | `write`

## Limitations
1. Currently the script only
support writing simple expenses, that is, any transaction with only two legs and
one of them is an expense.
2. The contacts like those in `change share <Contact>` are only searched by the leaf
   accounts under `...:Share:...`. For example,
   ```
   Liability:Share:Amy
   ```
   in the beancount file will indicate the presence of a contact named `Amy`.