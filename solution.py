import math

def find_optimal_travel_strategy(distance_km: int, available_lanes: int) -> dict:
    """
    Calculates the optimal strategy (minimum time, maximum people, and individual journey)
    to cover a given distance, based on the lane constraints.

    Args:
        distance_km: The total distance to be covered in km.
        available_lanes: The total number of highway lanes available.

    Returns:
        A dictionary containing the optimal Time, People, and Journey details.
    """
    if distance_km <= 0:
        return {
            "Error": "Distance must be greater than 0."
        }
    
    # 1. Calculate Maximum People (P)
    # Each person reserves 4 lanes (due to potential C4 usage).
    max_people = available_lanes // 4

    if max_people == 0:
        # If less than 4 lanes are available, only a single person can travel, 
        # but they must use a car that requires L lanes or less.
        # Following the strict rule that C4 is the fastest and the objective is optimal time, 
        # a minimum of 4 lanes is required for the most optimal strategy.
        # If we must provide an answer for L < 4, we assume the person uses the fastest available car.
        
        if available_lanes >= 3:
            fastest_car_speed = 300 # C3
            lanes_used = 3
            car_label = "C3"
        elif available_lanes >= 2:
            fastest_car_speed = 200 # C2
            lanes_used = 2
            car_label = "C2"
        elif available_lanes >= 1:
            fastest_car_speed = 100 # C1
            lanes_used = 1
            car_label = "C1"
        else:
            return {
                "Error": "Insufficient lanes. At least 1 lane required to start any journey.",
                "Time": "N/A",
                "People": 0
            }
        
        # Calculate time for one person using the fastest allowed car
        min_time = math.ceil(distance_km / fastest_car_speed)
        
        # Calculate the journey segments for the single person
        num_segments = min_time
        segment_distance = fastest_car_speed # Distance covered in 1 hour
        
        segments = []
        remaining_dist = distance_km
        for _ in range(num_segments - 1):
            segments.append(car_label)
            remaining_dist -= segment_distance
        
        # The last segment is the remainder
        if remaining_dist > 0:
            # Although the segment time is 1 hour, the last leg might be shorter distance
            # For simplicity and adhering to 1-hour segments:
            # Since Time = ceil(D/S), all segments must be 'S' except the last.
            # E.g., D=100, S=400. T=1. Segment is C4 (100km).
            segments.append(car_label)
        
        return {
            "Optimal Time (hours)": min_time,
            "Max People": 1,
            "Total Distance (km)": distance_km,
            "Available Lanes": available_lanes,
            "Journey Breakdown": {
                "Person 1": {
                    "Lanes Reserved": lanes_used,
                    "Route": " + ".join(segments),
                    "Total Distance Covered": distance_km
                }
            }
        }

    # 2. Calculate Minimum Time (T)
    # Max collective speed is 400 km/h per person.
    max_collective_speed = 400 * max_people
    min_time = math.ceil(distance_km / max_collective_speed)

    # 3. Calculate Journey Breakdown
    
    # Distance each person must cover to complete the trip in min_time
    # Note: This is D/P, rounded up to the nearest segment size if necessary,
    # but since Time is already calculated based on total distance, we use the average share.
    distance_share = distance_km / max_people
    
    journey_breakdown = {}
    
    # Due to ceil() function in Time, some people might cover slightly more/less than D/P
    # The total segments driven by all P people must equal max_collective_speed * min_time
    total_segments_required = max_collective_speed * min_time
    
    # Calculate the segments for the primary people
    # Total distance that needs to be covered is distance_km
    
    total_segments_needed = distance_km
    person_segment_target = distance_km // max_people # Target full segments
    remaining_total_dist = distance_km
    
    for i in range(1, max_people + 1):
        person_name = f"Person {i}"
        
        # Calculate the distance this person will cover (either D_share or slightly adjusted)
        # To simplify, we ensure the total distance is covered by assigning full segments (400km)
        # for all but the last remaining segments.
        
        # Each person covers D_share, rounded to nearest 400.
        dist_to_cover = min(remaining_total_dist, math.ceil(distance_share / 400) * 400)
        
        if remaining_total_dist <= 0:
            dist_to_cover = 0
            
        full_c4_segments = dist_to_cover // 400
        remaining_dist_segment = dist_to_cover % 400
        
        route_segments = []
        
        # Full C4 segments (1 hour each)
        for _ in range(full_c4_segments):
            route_segments.append("C4 (400 km)")

        # Final segment for the remainder (must be completed in the final hour)
        if remaining_dist_segment > 0:
            if remaining_dist_segment == 100:
                route_segments.append("C1 (100 km)")
            elif remaining_dist_segment == 200:
                route_segments.append("C2 (200 km)")
            elif remaining_dist_segment == 300:
                route_segments.append("C3 (300 km)")
            # No need for else: it's handled by full_c4_segments
            
        # If the total required time (T) is longer than the required segments for D_share,
        # the person must wait or drive less (not applicable for optimal strategy)
        
        total_dist_covered_by_person = full_c4_segments * 400 + remaining_dist_segment
        remaining_total_dist -= total_dist_covered_by_person
        
        # If the person has finished their part but Time > 1, they must wait.
        if not route_segments and min_time > 0:
            # This person is not needed for the journey
            continue

        journey_breakdown[person_name] = {
            "Lanes Reserved": 4,
            "Route": " + ".join(route_segments),
            "Total Distance Covered": total_dist_covered_by_person
        }
        
    return {
        "Optimal Time (hours)": min_time,
        "Max People": max_people,
        "Total Distance (km)": distance_km,
        "Available Lanes": available_lanes,
        "Journey Breakdown": journey_breakdown
    }

# --- Examples ---

# Example 1: D=1000, L=4
print("--- Example 1: D=1000 km, L=4 ---")
result1 = find_optimal_travel_strategy(1000, 4)
print(f"Optimal Time: {result1['Optimal Time (hours)']} hours")
print(f"Max People: {result1['Max People']}")
print(f"Journey: {result1['Journey Breakdown']['Person 1']['Route']}")
# Expected: Time: 3, People: 1, Journey: C4 + C4 + C2

print("\n--- Example 2: D=800 km, L=8 (Optimal Derivation) ---")
result2 = find_optimal_travel_strategy(800, 8)
print(f"Optimal Time: {result2['Optimal Time (hours)']} hours")
print(f"Max People: {result2['Max People']}")
print(f"Journey P1: {result2['Journey Breakdown']['Person 1']['Route']}")
print(f"Journey P2: {result2['Journey Breakdown']['Person 2']['Route']}")
# Expected: Time: 1, People: 2, Journey: C4 + C4

print("\n--- Example 3: D=1500 km, L=6 ---")
result3 = find_optimal_travel_strategy(1500, 6)
print(f"Optimal Time: {result3['Optimal Time (hours)']} hours")
print(f"Max People: {result3['Max People']}")
print(f"Journey: {result3['Journey Breakdown']['Person 1']['Route']}")
# Expected: Time: 4, People: 1 (L=6 -> P=1)

