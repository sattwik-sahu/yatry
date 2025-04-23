import pulp

class VehicleAssignmentModel:
    def __init__(self, groups, segment_costs, capacity=5):
        self.CAPACITY = capacity
        self.segment_costs = segment_costs
        self.M_val = sum(segment_costs)
        self._prepare_trips(groups)
        self._define_sets()

    @staticmethod
    def _split_group(group, capacity):
        count = group['count']
        if count <= capacity:
            return [group]
        sub = []
        full, rem = divmod(count, capacity)
        for _ in range(full):
            sub.append({**group, 'count': capacity})
        if rem:
            sub.append({**group, 'count': rem})
        return sub

    def _prepare_trips(self, groups):
        self.trips = []
        for g in groups:
            self.trips.extend(self._split_group(g, self.CAPACITY))

    def _define_sets(self):
        # Stops and segments
        max_drop = max(t['drop'] for t in self.trips)
        self.segments = list(range(1, max_drop))
        # Vehicles and trip indices
        self.T = list(range(len(self.trips)))
        self.V = list(range(len(self.trips)))
        # Trips active on each segment
        self.T_seg = {s: [] for s in self.segments}
        for t in self.T:
            pu, dr = self.trips[t]['pickup'], self.trips[t]['drop']
            for s in self.segments:
                if pu <= s < dr:
                    self.T_seg[s].append(t)

    def build_model(self):
        self.model = pulp.LpProblem('VehicleAssignment', pulp.LpMinimize)
        # Decision vars
        x = {(t,v): pulp.LpVariable(f'x_{t}_{v}', cat='Binary')
             for t in self.T for v in self.V}
        y = {(v,s): pulp.LpVariable(f'y_{v}_{s}', cat='Binary')
             for v in self.V for s in self.segments}
        occ = {(v,s): pulp.LpVariable(f'occ_{v}_{s}', lowBound=0, cat='Integer')
               for v in self.V for s in self.segments}
        gamma = {(v,s,k): pulp.LpVariable(f'gamma_{v}_{s}_{k}', cat='Binary')
                 for v in self.V for s in self.segments for k in range(1, self.CAPACITY+1)}
        F = {t: pulp.LpVariable(f'F_{t}', lowBound=0) for t in self.T}
        Z = pulp.LpVariable('Z', lowBound=0)

        # Constraints
        for v in self.V:
            for s in self.segments:
                self.model += pulp.lpSum(self.trips[t]['count']*x[(t,v)] for t in self.T_seg[s]) <= self.CAPACITY*y[(v,s)]
                if self.T_seg[s]:
                    self.model += pulp.lpSum(x[(t,v)] for t in self.T_seg[s]) <= len(self.T_seg[s])*y[(v,s)]
                self.model += occ[(v,s)] == pulp.lpSum(self.trips[t]['count']*x[(t,v)] for t in self.T_seg[s])
                self.model += pulp.lpSum(gamma[(v,s,k)] for k in range(1,self.CAPACITY+1)) == y[(v,s)]
                self.model += occ[(v,s)] == pulp.lpSum(k*gamma[(v,s,k)] for k in range(1,self.CAPACITY+1))

        for t in self.T:
            self.model += pulp.lpSum(x[(t,v)] for v in self.V) == 1
            for v in self.V:
                S_t = [s for s in self.segments if self.trips[t]['pickup'] <= s < self.trips[t]['drop']]
                f_vt = pulp.lpSum(
                    self.segment_costs[s-1] * pulp.lpSum((1.0/k)*gamma[(v,s,k)]
                                                         for k in range(1,self.CAPACITY+1))
                    for s in S_t)
                self.model += F[t] >= f_vt - self.M_val*(1-x[(t,v)])
                self.model += F[t] <= f_vt + self.M_val*(1-x[(t,v)])
            self.model += F[t] <= Z

        self.model += Z

        # store for external use
        self.x, self.y, self.occ, self.gamma, self.F, self.Z = x, y, occ, gamma, F, Z
        return self.model

    def solve(self, **kwargs):
        self.model.solve(**kwargs)
        # Extract assignments
        self.assignments = {v: [t for t in self.T if pulp.value(self.x[(t,v)])>0.5]
                             for v in self.V if any(pulp.value(self.x[(t,v)])>0.5 for t in self.T)}
        self.Z_val = pulp.value(self.Z)
        return pulp.LpStatus[self.model.status]

    def get_results(self):
        used_vs = sorted(self.assignments.keys())              # e.g. [3,7]
        v_map   = {v: idx+1 for idx, v in enumerate(used_vs)}  # {3:1, 7:2}
        details = []
    
        for v, trips in self.assignments.items():
            seq_v = v_map[v]           # 1 or 2
            # … then build your record using seq_v instead of v+1 …
            for t in trips:
                details.append({
                    'vehicle':    seq_v,
                    'group':      self.trips[t]['id'],
                    'pickup':     self.trips[t]['pickup'],
                    'drop':       self.trips[t]['drop'],
                    'count':      self.trips[t]['count'],
                    'fare':       pulp.value(self.F[t]),
                    'occ':        {s: pulp.value(self.occ[(v,s)]) for s in self.segments if pulp.value(self.y[(v,s)])>0.5}
                })
        return {'Z': pulp.value(self.Z), 'details': details}
