# BoilerSignal (Purdue University)
## Estimation of Site-Specific Radio Propagation Loss Estimation with Minimal Information
### ITU AI/ML in 5G Challenge

**Authors:**  
Manish Kumar  
Ahmed P. Mohamed  
PhD Candidates, Purdue University (at the time of the competition)

Team BoilerSignal finished 4th in the ITU AI/ML in 5G Challenge
---

## 1. Introduction

This repository contains the complete solution developed by **Team BoilerSignal (Purdue University)** for the **ITU AI/ML in 5G Challenge: Estimation of Site-Specific Radio Propagation Loss Estimation with Minimal Information**.

The challenge, organized by the International Telecommunication Union (ITU) under the AI for Good initiative, focused on developing machine learning models for estimating **urban radio propagation loss (PL)** using limited geometric and environmental information.

Official challenge page:  
https://challenge.aiforgood.itu.int/match/matchitem/112

---

## 2. Problem Formulation

Urban radio propagation loss depends on multiple factors:

- Line-of-sight (LOS) and non-line-of-sight (NLOS) conditions  
- Building obstruction and diffraction  
- Frequency-dependent behavior  
- Transmitter (Tx) and receiver (Rx) geometry  
- Multipath propagation  

Participants were provided with:

- A detailed 3D mesh (OBJ format) of a region in Tokyo  
- Tx–Rx coordinate pairs  
- Ground-truth propagation loss values for three frequency bands:
  - 800 MHz  
  - 7 GHz  
  - 28 GHz  

The objective was to predict propagation loss for unseen Tx–Rx pairs without performing computationally expensive ray-tracing simulations.

---

## 3. Methodology Overview

Our solution is based on **geometry-aware feature extraction combined with machine learning regression models**.

### 3.1 Geometric Region Extraction

For each Tx–Rx pair, we extracted localized geometric regions from the 3D city mesh:

1. TX-centered sphere (50 m radius)
2. RX-centered sphere (50 m radius)
3. 1st Fresnel ellipsoid
4. 3rd Fresnel ellipsoid

These regions capture:

- Local obstruction density  
- Fresnel zone blockage  
- Diffraction-relevant structures  
- Near-field scattering environment  

Mesh clipping operations were performed to isolate only the surfaces intersecting these regions.

---

### 3.2 Feature Engineering

From the clipped regions, we computed structured geometric descriptors including:

- Number of intersecting faces  
- Obstruction counts between Tx and Rx  
- LOS/NLOS indicator  
- Tx–Rx distance  
- Frequency-derived wavelength  
- Fresnel obstruction metrics  
- Height-related features  

These features form a compact geometric representation of the propagation environment.

---

### 3.3 Learning Approaches

We explored two modeling paradigms:

#### A. PointNet-Based Deep Learning

- Converted clipped mesh surfaces to point clouds  
- Trained PointNet to learn geometric embeddings  
- Used embeddings as additional propagation features  

#### B. Gradient Boosting (Final Model)

- Trained CatBoost regressors using engineered geometric features  
- Achieved superior stability and performance  
- Selected as the final submission model  

The final solution uses **CatBoost regression over geometry-derived features**.

---

## 4. Repository Structure

### Data Directories

#### `a_3DMap_Data/`
Tokyo 3D city mesh provided by the competition organizers.

#### `b_training_propagation_loss/`
Training datasets for:
- 800 MHz  
- 7 GHz  
- 28 GHz  

Each file contains Tx–Rx coordinates and true propagation loss values.

#### `c_evaluation_propagation_loss/`
Evaluation dataset used for final submission generation.

#### `catboost_training/`
Processed feature datasets used for CatBoost training.

#### `results_pl_competition/`
Final prediction outputs and submission files.

#### `satellite-imagery-downloader/`
Initial exploration of satellite imagery integration for propagation modeling.  
This direction was later discontinued in favor of 3D mesh geometry alone.  
Multimodal fusion (satellite imagery + 3D geometry) remains a promising future research direction.

---

### Core Notebooks

1. `1_map_fresnel_ellipse_experiments.ipynb`  
   - Mesh visualization  
   - Sphere and Fresnel region extraction  
   - Geometric clipping experiments  

2. `2_generate_portable_mesh.ipynb`  
   - Converts OBJ mesh into `portable_mesh.npz` for efficient processing  

3. `3_generate_3d_geometry_dataset.ipynb`  
   - Extracts TX/RX spheres and 1st & 3rd Fresnel zones for all frequencies  

4. `4_PL_estimation_with_pointnet_experiments.ipynb`  
   - Point cloud extraction  
   - PointNet experiments  

5. `5_PL_estimation_with_pointnet.ipynb`  
   - Full PointNet training pipeline  

6. `6_folder_pre_processing.ipynb`  
   - Structured feature extraction  
   - LOS/NLOS analysis  
   - Obstruction statistics  

7. `7_Catboost_All.ipynb`  
   - Full-feature CatBoost training  

8. `7_Catboost_Subset.ipynb`  
   - Feature subset experiments  

9. `8_post_catboost_training_processing.ipynb`  
   - Prediction aggregation  
   - Submission preparation  

---

### Key Files

- `portable_mesh.npz` – Optimized mesh for repeated geometry processing  
- `Estimation_of_Site_specific_radio_propagation_loss_with_minimal_information.pdf` – Final technical report  
- `KDDI_Certificate_for_participation.pdf` – Official ITU certificate  

---

## 5. Contributions

This work demonstrates that:

- Detailed ray tracing is not strictly necessary for competitive propagation estimation.  
- Carefully designed geometric abstractions can encode key propagation phenomena.  
- Classical gradient boosting methods remain highly effective when features are physically informed.  

The solution bridges:

- Computational geometry  
- Wireless propagation theory  
- Machine learning regression  

---

## 6. Future Directions

Potential extensions include:

- Multimodal learning using satellite imagery + 3D geometry  
- Graph neural networks on mesh topology  
- Point Transformer architectures  
- Physics-informed neural networks  
- Transfer learning across urban environments  
- Multi-frequency joint modeling  

---

## 7. Authors (affiliation at the time of the competition)

**Manish Kumar**  
PhD Candidate  
Purdue University  

**Ahmed P. Mohamed**  
PhD Candidate  
Purdue University  

Team Name: **BoilerSignal**

---

## 8. Acknowledgment

We acknowledge the International Telecommunication Union (ITU) and the AI for Good initiative for organizing the AI/ML in 5G Challenge and providing the datasets used in this work.

---

## 9. Citation

If this repository contributes to your research, please cite:

BoilerSignal (Purdue University),  
*Estimation of Site-Specific Radio Propagation Loss with Minimal Information*,  
ITU AI/ML in 5G Challenge.

---
