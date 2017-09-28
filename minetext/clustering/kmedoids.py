from random import shuffle


class Kmedoids(object):
    def __init__(self, k, tweets, distance_calculator, text_field_name='text', k_min=1, k_max=None, max_err=None):
        self.distance_calculator = distance_calculator
        self.k = k
        self.clusters = []
        self.tweets = tweets
        self.max = float("inf")
        self.init_clusters()
        self.set_random_medoids()
        self.k_min = k_min
        self.k_min_init = self.k_min
        self.k_max = k_max
        self.max_err = max_err
        self.text_field_name = text_field_name

    def init_clusters(self):
        for i in range(self.k):
            cluster = dict()
            cluster['id'] = i
            cluster['medoid'] = None
            cluster['tweets'] = []
            self.clusters.append(cluster)

    def set_random_medoids(self):
        possible_medoids = []
        for i in range(len(self.tweets)):
            possible_medoids.append(i)

        shuffle(possible_medoids)

        for j in range(self.k):
            medoid = self.tweets[possible_medoids[j]]
            medoid['cluster'] = j
            self.clusters[j]['medoid'] = medoid

    def clear_clusters(self):
        for cluster in self.clusters:
            cluster['tweets'] = []

    def get_medoids(self):
        medoids = []
        for cluster in self.clusters:
            medoid = cluster['medoid']
            medoid['cluster'] = cluster['id']
            medoids.append(medoid)

        return medoids

    def assign_cluster(self):
        min_dist = self.max
        self.clear_clusters()
        medoids = self.get_medoids()
        cluster_id = -1

        for i in range(len(self.tweets)):
            for j in range(len(medoids)):
                distance = self.distance_calculator.calculate(self.tweets[i][self.text_field_name], medoids[j][self.text_field_name])
                if distance < min_dist:
                    min_dist = distance
                    cluster_id = medoids[j]['cluster']

            self.tweets[i]['cluster'] = cluster_id
            self.get_cluster_by_id(cluster_id)['tweets'].append(self.tweets[i])
            cluster_id = -1
            min_dist = self.max

    def calculate_medoids(self):
        dist = self.max
        medoids = []
        for i in range(len(self.clusters)):
            tweets = self.clusters[i]['tweets']
            tweets.append(self.clusters[i]['medoid'])
            for j in range(len(tweets)):
                acc_distance = 0.0
                for k in range(len(tweets)):
                    if not tweets[j]['id'] == tweets[k]['id']:
                        acc_distance += self.distance_calculator.calculate(tweets[j][self.text_field_name], tweets[k][self.text_field_name])

                mean = acc_distance / (len(tweets))

                if mean < dist:
                    dist = mean
                    self.clusters[i]['medoid'] = tweets[j]

            self.clusters[i]['medoid']['cluster'] = self.clusters[i]['id']
            medoids.append(self.clusters[i]['medoid'])
            dist = self.max
        return medoids

    def get_cluster_by_id(self, cluster_id):
        for i in range(len(self.clusters)):
            if self.clusters[i]['id'] == cluster_id:
                return self.clusters[i]
        return None

    def clustering(self):
        self.assign_cluster()
        self.calculate_medoids()
        return self.clusters

    def calculate_partial_sse(self):
        distance = 0
        for cluster in self.clusters:
            for tweet in cluster['tweets']:
                distance += self.distance_calculator.calculate(tweet[self.text_field_name], cluster['medoid'][self.text_field_name])
        return distance

    def calculate_elbow(self):
        original_k = self.k
        sse = dict()
        for k in range(self.k_min_init, self.k_max):
            self.k = k
            self.assign_cluster()
            self.calculate_medoids()
            sse[k] = self.calculate_partial_sse()
        self.k = original_k
        return sse
