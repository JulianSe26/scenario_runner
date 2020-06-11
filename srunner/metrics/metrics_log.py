import carla


class MetricsLog(object):
    """
    Utility class to query the metrics log. The information of
    the log must be accesed through the functions:
    """

    def __init__(self, recorder, criteria):
        """
        Initializes the log class and parses it to extract the disctionaries
        """
        self._actors_info = recorder[0]
        self._simulation_info = recorder[1][1:]
        self._general_info = recorder[1][0]
        self._criteria = criteria

    def get_actor_state(self, actor_id, frame, variable):
        """
        Given an actor id, returns the specific variable of that actor at a given frame.
        Returns None if the log doesn't have the actor_id or if the attribute is missing.
        The variable can be one of the follwoing:
            - transform: (for vehicles and walkers)
            - velocity: (for vehicles)
            - control: (for vehicles)
            - speed: (for walkers)
            - state: (for traffic lights)
            - frozen: (for traffic lights)
            - elapsed_time: (for traffic lights)

        Args:
            actor_id (int): Id of the actor to be checked
            frame: (int): frame number of the simulation
            attribute (str): name of the actor's attribute to be returned

        """
        frame_state = self._simulation_info[frame]["actors"]
        if actor_id in frame_state:

            if variable not in frame_state[actor_id]:
                print("WARNING: Can't find {} for actor with ID {}".format(variable, actor_id))
                return None
        
            variable_info = frame_state[actor_id][variable]
            return variable_info
        return None
    
    def get_all_actor_states(self, actor_id, variable, ini_frame=None, end_frame=None):
        """
        Given an actor id, returns a list of the specific variable of that actor during
        a frame interval. This function uses get_actor_state, so some of elements might
        be None.

        Args:
            actor_id (int): ID of the actor
            attribute: name of the actor's attribute to be returned
            ini_frame (int): First frame checked. By default, 0 
            end_frame (int): Last frame checked. By default, max number of frames.
        """
        if ini_frame is None:
            ini_frame = 0
        if end_frame is None:
            end_frame = len(self._simulation_info) - 1

        variable_list = []

        for frame_number in range(ini_frame, end_frame + 1):

            variable_info = self.get_actor_state(actor_id, frame_number, variable)
            variable_list.append(variable_info)

        return variable_list

    def get_collisions(self, actor_id):
        """
        Returns a dictionary containing the frames at which the actor collided
        and the id of the other actor (dict{frame number - other actor ID})

        Args:
            actor_id (int): ID of the actor
        """
        collisions = {}

        for i, frame_state in enumerate(self._simulation_info):
            if actor_id in frame_state["collisions"]:
                collisions.update({i: frame_state["collisions"][actor_id]})
        return collisions

    def get_ego_vehicle_id(self):
        """
        Returns an int with the id of the ego vehicle.
        """
        return get_actor_id_with_role_name("hero")

    def get_actor_ids_with_role_name(self, rolename):
        """
        Returns an int with the actor's id of the one with a specific rolename
        Useful for identifying special actors such as the ego vehicle

        Args:
            role_name (str): string with the desired rolename to filter the actors
        """
        actor_list = []

        for actor_id in self._actors_info:

            actor_info = self._actors_info[actor_id]
            if "role_name" in actor_info and actor_info["role_name"] == rolename:
                actor_list.append(actor_id)

        return actor_list
        
    def get_actor_ids_with_type_id(self, type_id):
        """
        Returns an int with the actor's id of the one with a specific type_id

        Args:
            type_id (str): string with the desired type id to filter the actors
        """
        actor_list = []

        for actor_id in self._actors_info:

            actor_info = self._actors_info[actor_id]
            if "type_id" in actor_info and actor_info["type_id"] == rolename:
                actor_list.append(actor_id)

        return actor_list
    
    def get_actor_attributes(self, actor_id):
        """
        Returns all the blueprint attributes of an actor

        Args:
            actor_id (int): Id of the actor from which the information will be returned
        """
        if actor_id in self._actors_info:
            return self._actors_info[actor_id]

        return None

    def get_actor_alive_frames(self, actor_id):
        """
        Returns a tuple with the first and last frame an actor was alive.

        Args:
            actor_id (int): Id of the actor from which the information will be returned
        """

        if actor_id in self._actors_info:

            actor_info = self._actors_info[actor_id]
            first_frame = actor_info ["created"]
            if "destroyed" in actor_info:
                last_frame = actor_info ["destroyed"]
            else:
                last_frame = self.get_total_frame_count()

            return first_frame, last_frame
        
        return None, None

    def get_criterion(self, name):
        """
        Returns a dictionary with the attributes of the criterion.

        Args:
            name (str): name of the criterion
        """
        if name in self._criteria:
            return self._criteria[name]

        return None

    def get_total_frame_count(self):
        """
        Returns an int with the total amount of frames the simulation lasted
        """

        return self._general_info["total_frames"]
