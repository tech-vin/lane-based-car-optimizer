# 🏎️ Car Optimization Problem — Interview Scenario

## 🧩 Problem Statement

You are given a set of cars and a multi-lane highway.  
Each car type has a fixed **distance capacity (in km)** per full tank, and occupies a fixed number of **lanes** when traveling.

There are **4 types of cars:**

| Car | Range per Full Tank (km) | Lanes Occupied |
|------|---------------------------|----------------|
| 🚗 **C1** | 100 | 1 |
| 🚙 **C2** | 200 | 2 |
| 🏎️ **C3** | 300 | 3 |
| 🚐 **C4** | 400 | 4 |

---

## 🚘 Conditions

1. The user provides two inputs:
   - **Distance (int)** → total distance to be covered (e.g., 1000 km)
   - **Lanes (int)** → total number of lanes available on the highway (e.g., 4, 6, etc.)

2. Each car can travel only **up to its full-tank range**  
   (e.g., C3 → 300 km per run).  
   After completing that distance, it must **refuel** at its corresponding station before continuing.

3. Refueling stations are located at:
   - Every **100 km** for C1  
   - Every **200 km** for C2  
   - Every **300 km** for C3  
   - Every **400 km** for C4  

   Cars can refuel and move ahead, or be switched to another car type only at these checkpoints.

4. Each car can carry **only 1 person**.

5. At any given moment, the **total number of lanes occupied** by all active cars must **not exceed** the available lane count provided by the user.

6. The goal is to determine the **most optimized combination of cars** and **their scheduling** such that:
   - The **total distance** is covered completely, and  
   - The **lane usage constraint** is never violated.

---

## 🧠 Clarifications

- “**Full capacity**” means a car must travel its entire range before stopping or switching.  
  For example, C4 must always complete **exactly 400 km** before refueling or being replaced.

- Switching between car types is allowed **only at refueling checkpoints**.

- Optimization can be interpreted as:
  - ⏱️ **Minimum total time** to cover the full distance  
  - 🛣️ **Maximum utilization** of available lanes (efficiency)  
  - 👥 **Maximum number of people** traveling simultaneously  

---

## 🎯 Example Scenario

If:
- **Distance = 1000 km**
- **Lanes = 6**

Then one possible **optimized plan** could be:

| Hour | Cars Used | Distance Covered | Lanes Used |
|------|------------|------------------|-------------|
| 1️⃣ | 🏎️ C3 + 🏎️ C3 | 600 km | 6 |
| 2️⃣ | 🚐 C4 | 400 km | 4 |

✅ **Total Distance Covered:** 1000 km  
✅ **Total Time Taken:** 2 hours  
✅ **Total People Traveling:** 3  
✅ **Lane Limit:** Not exceeded (max 6 lanes used at any time)

---

### 🔄 Alternate Valid Plans

Other combinations can also achieve 1000 km (e.g., using multiple C1 or C2 cars)  
as long as:
- Each car runs its **full capacity** per turn, and  
- The total **lanes in use ≤ available lanes**.

---

### 🧮 Optimization Summary

This problem can be modeled as:
- A **combinatorial scheduling** or **bin-packing** problem, where each car run consumes a certain number of lanes (like bin space) for 1 time unit (hour).  
- The objective is to **minimize total time** (number of time slots) while ensuring that the **sum of all car distances equals the total target distance**.
