## Development Journal
- **Best Model**: Best performing model is discovered as layers=[256,128,32]



### Experiments

#### January 7th  
- **Null Data Representation (0 dB)**
  - Achieved **76.22% accuracy**. later **60.78% accuracy (9th Jan)**  
- **Null Data Representation (-100 dB)**:  
  - Achieved **74.00% accuracy**.  
- **Null Data Representation (-999 dB)**:  
  - Achieved **77.78% accuracy**.

#### January 9th  
- **Data Augmentation**:  
  - Accuracy increased to **69.44%** (from 60.78)
- **Switched to Loss Calculation**:  
  - **Baseline Test Loss**: 0.107507
  - **Augmented data loss**: 0.157616

---
### Notes
- **Next Steps**: Focus on obtaining more diverse data to improve generalization.
- **Priority**: Continue monitoring both loss and accuracy for better insight into model performance.