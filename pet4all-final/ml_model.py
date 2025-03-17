import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics.pairwise import cosine_similarity


def recommend_dog_breeds(user_features_normalized, kmeans, dog_dataset, user_features_columns):
    # Predict user cluster (extract the cluster index from the array)
    user_cluster = kmeans.predict(user_features_normalized[:, :6])[0]  # [0] to get the index

    # Dog breeds in the same cluster as the user
    recommended_dog_breeds = dog_dataset[kmeans.labels_ == user_cluster]

    # Filter columns to match the original order
    recommended_dog_breeds = recommended_dog_breeds[user_features_columns + ['breed']]

    return recommended_dog_breeds


def collaborative_filtering(user_features_normalized, dog_features_normalized, dog_dataset):
    # Calculate cosine similarity between user and dog breed features
    similarity_matrix = cosine_similarity(user_features_normalized, dog_features_normalized)

    # Get indices of top 5 similar dog breeds
    similar_dog_indices = similarity_matrix.argsort(axis=1)[:, ::-1][0][:5]

    # Get top similar dog breeds and their similarity percentages
    top_similar_dog_breeds = dog_dataset['breed'].iloc[similar_dog_indices]
    similarity_percentages = (similarity_matrix[0][similar_dog_indices] * 100).round(2)

    # Create DataFrame with results
    recommended_dog_breeds_collab = pd.DataFrame({'breed': top_similar_dog_breeds, 'similarity_percentage': similarity_percentages})

    return recommended_dog_breeds_collab


def make_recommendation(user_data):
    grooming = float(user_data['grooming']) + float(user_data['grooming_preference']) + float(user_data['minimal_grooming'])
    shedding = float(user_data['shedding']) + float(user_data['shedding_preference']) + float(user_data['manage_shedding'])
    energy = float(user_data['energy_level']) + float(user_data['daily_exercise']) + float(user_data['outdoor_activities'])
    trainability = float(user_data['trainability']) + float(user_data['obedience_training']) + float(user_data['quick_learning'])
    demeanor = float(user_data['demeanor']) + float(user_data['playful']) + float(user_data['reserved'])
    size = float(user_data['size_of_living_space']) + float(user_data['preferred_size']) + float(user_data['indoor_space'])

    user_features = {
        'grooming': grooming / 3,
        'shedding': shedding / 3,
        'energy': energy / 3,
        'trainability': trainability / 3,
        'demeanor': demeanor / 3,
        'size': size / 3,
    }

    return pd.DataFrame(user_features, index=[0])


def get_recommendations(user_data):
    # Load dog dataset
    dog_dataset = pd.read_csv('datasets/dog_breed.csv')

    # Select features for clustering and filtering
    user_features_columns = ['grooming', 'shedding', 'energy', 'trainability', 'demeanor', 'size']
    dog_features = dog_dataset[['grooming', 'shedding', 'energy', 'trainability', 'demeanor', 'size']]

    # Convert user data to user features
    user_features_df = make_recommendation(user_data)

    # Numeric data types
    user_features_df = user_features_df.apply(pd.to_numeric, errors='coerce')

    # Handle missing values
    user_features_df = user_features_df.fillna(user_features_df.mean())
    dog_features = dog_features.fillna(dog_features.mean())

    # Normalize features to [0, 1]
    scaler = MinMaxScaler()
    dog_features_normalized = scaler.fit_transform(dog_features)

    # Train KMeans model
    kmeans = KMeans(n_clusters=5)
    kmeans.fit(dog_features_normalized)

    # Normalize user features
    user_features_normalized = scaler.transform(user_features_df.values)

    # Predict user cluster (extract the cluster index from the array)
    user_cluster = kmeans.predict(user_features_normalized[:, :6])[0]  # [0] to get the index

    # Get recommendations based on clustering
    recommended_dog_breeds_cluster = recommend_dog_breeds(user_features_normalized, kmeans, dog_dataset, user_features_columns)

    # Sort recommended breeds within cluster by cosine similarity to user features
    similarities = cosine_similarity(user_features_normalized, dog_features_normalized[kmeans.labels_ == user_cluster])
    recommended_dog_breeds_cluster = recommended_dog_breeds_cluster.iloc[similarities.argsort(axis=1)[:, ::-1][0][:5]]

    # Get recommendations based on collaborative filtering
    recommended_dog_breeds_collab = collaborative_filtering(user_features_normalized, dog_features_normalized, dog_dataset)

    return recommended_dog_breeds_cluster, recommended_dog_breeds_collab


if __name__ == "__main__":
    # Example usage when running the file independently
    user_data_example = {
        'grooming': 0.5,
        'grooming_preference': 0.5,
        'minimal_grooming': 0.5,
        'shedding': 0.5,
        'shedding_preference': 0.5,
        'manage_shedding': 0.5,
        'energy_level': 0.5,
        'daily_exercise': 0.5,
        'outdoor_activities': 0.5,
        'trainability': 0.5,
        'obedience_training': 0.5,
        'quick_learning': 0.5,
        'demeanor': 0.5,
        'playful': 0.5,
        'reserved': 0.5,
        'size_of_living_space': 0.5,
        'preferred_size': 0.5,
        'indoor_space': 0.5,
    }

    recommendations_cluster, recommendations_collab = get_recommendations(user_data_example)

    print("Recommended Dog Breeds (Clustering):")
    print(recommendations_cluster)

    print("\nTop Similar Dog Breeds (Collaborative Filtering):")
    print(recommendations_collab)
