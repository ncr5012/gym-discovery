from gym.envs.registration import register

register(
    id='discovery-v0',
    entry_point='gym_discovery.envs:DiscoveryEnv',
)
