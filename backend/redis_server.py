import redis

class RedisServer:

    def __init__(self):
        self.redis = redis.Redis(host='localhost', port=6379, db=0)

    def get_game(self, game_id):
        return self.redis.get(game_id)
    
    def set_game(self, game_id, game_data):
        # Convert Game object to dictionary if it's not already one
        if hasattr(game_data, '__dict__'):
            game_data = game_data.__dict__
        self.redis.hset(game_id, mapping=game_data)

    def check_game_exists(self, game_id):
        if self.redis.exists(game_id):
            return True
        else:
            return False
    

