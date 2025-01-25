# Results (from ToxiGuard.ipynb)
| Label           | Loss  | Accuracy | Precision | Recall  |
|-----------------|-------|----------|-----------|---------|
| toxic           | 5.37% | 98.27%   | 98.19%    | 98.34%  |
| obscene         | 2.42% | 99.20%   | 99.24%    | 99.17%  |
| threat          | 0.84% | 99.76%   | 99.91%    | 99.61%  |
| insult          | 1.72% | 99.37%   | 99.44%    | 99.29%  |
| identity_hate   | 0.64% | 99.77%   | 99.74%    | 99.80%  |

### Key Definitions

- **Precision**: The proportion of correctly identified positive cases out of all predicted positive cases. Higher precision ensures fewer false positives.
- **Recall**: The proportion of correctly identified positive cases out of all actual positive cases. Higher recall ensures fewer false negatives.
- **Accuracy**: The proportion of correctly classified messages (both positive and negative) out of all messages.

### Observations
- Very good results overall!

# How it works


# Pain Points and challenges


# Future Enhancements

To improve the bot's classification accuracy:
1. Fine tune the bot for racist comments
2. Expand the training dataset to include more real-world Discord messages.
3. Train model for detecting toxic abbreviations
