# Strategy: Use the inspected Pipe-16 HybridOpening controller. Reassign idle workers during the first three days to plant, water and harvest one temporary wheat crop, then restore the planned pasture and deliver the wheat. Preserve the public Metav4 production and market controller. This is attributed reuse, and its stronger public source still needs live confirmation. Disable optional environment-dependent external library loading so the archive is self-contained.
# Local packaging modifications, 2026-09-20. Original attribution retained.
# Kaggriculture submission v9/3: public V39 (Apache-2.0, notices below) plus the v9 layers
# RACEPX gate, RACE (reservation from step 192, horizon 40 / margin 12), COURIER, CARROT and HERD
# appended at the end of this file.
# EXP-173 isolate opening market sequence inspired by yhay81/shop-router-0911-simple (Apache-2.0).
# Kaggriculture EXP-167 candidate. Not submitted automatically.
# Attribution: thomastschinkel, yhay81, destbreso, aurax7, tetsutani,
# prvsiyan and Dmitrii Gluzdov. Apache-2.0 derivations; notices retained below.
# Kaggriculture v31 / EXP-157, Ahmed Berat Ozer, September 9 2026.
# Selected mechanism: crop_public_order. New independent confirmation is required.
# Public V221B/V224C production/timing lineage: prvsiyan, Apache-2.0.
# Original economics and integration; retained upstream licenses follow.
# Kaggriculture v28 / EXP-154, Ahmed Berat Ozer, September 9 2026.
# Changes: aurax7 day-end storage guard; Dmitrii Gluzdov physical terminal rescue
# adapted to v27, with 64 deterministic simulations. Apache-2.0.
# New action tapes and ordered shop-pair map: yhay81/shop-router-0909, Apache-2.0.
# Kaggriculture v25, EXP-149: Shop0908 production, sale lead, terminal cargo rescue.
# Runtime chassis: Apache-2.0; thomastschinkel, yhay81, tetsutani.
# Routing and public action data: yhay81/shop-router-0908, frozen September 8, 2026.
# 
#                                  Apache License
#                            Version 2.0, January 2004
#                         http://www.apache.org/licenses/
# 
#    TERMS AND CONDITIONS FOR USE, REPRODUCTION, AND DISTRIBUTION
# 
#    1. Definitions.
# 
#       "License" shall mean the terms and conditions for use, reproduction,
#       and distribution as defined by Sections 1 through 9 of this document.
# 
#       "Licensor" shall mean the copyright owner or entity authorized by
#       the copyright owner that is granting the License.
# 
#       "Legal Entity" shall mean the union of the acting entity and all
#       other entities that control, are controlled by, or are under common
#       control with that entity. For the purposes of this definition,
#       "control" means (i) the power, direct or indirect, to cause the
#       direction or management of such entity, whether by contract or
#       otherwise, or (ii) ownership of fifty percent (50%) or more of the
#       outstanding shares, or (iii) beneficial ownership of such entity.
# 
#       "You" (or "Your") shall mean an individual or Legal Entity
#       exercising permissions granted by this License.
# 
#       "Source" form shall mean the preferred form for making modifications,
#       including but not limited to software source code, documentation
#       source, and configuration files.
# 
#       "Object" form shall mean any form resulting from mechanical
#       transformation or translation of a Source form, including but
#       not limited to compiled object code, generated documentation,
#       and conversions to other media types.
# 
#       "Work" shall mean the work of authorship, whether in Source or
#       Object form, made available under the License, as indicated by a
#       copyright notice that is included in or attached to the work
#       (an example is provided in the Appendix below).
# 
#       "Derivative Works" shall mean any work, whether in Source or Object
#       form, that is based on (or derived from) the Work and for which the
#       editorial revisions, annotations, elaborations, or other modifications
#       represent, as a whole, an original work of authorship. For the purposes
#       of this License, Derivative Works shall not include works that remain
#       separable from, or merely link (or bind by name) to the interfaces of,
#       the Work and Derivative Works thereof.
# 
#       "Contribution" shall mean any work of authorship, including
#       the original version of the Work and any modifications or additions
#       to that Work or Derivative Works thereof, that is intentionally
#       submitted to Licensor for inclusion in the Work by the copyright owner
#       or by an individual or Legal Entity authorized to submit on behalf of
#       the copyright owner. For the purposes of this definition, "submitted"
#       means any form of electronic, verbal, or written communication sent
#       to the Licensor or its representatives, including but not limited to
#       communication on electronic mailing lists, source code control systems,
#       and issue tracking systems that are managed by, or on behalf of, the
#       Licensor for the purpose of discussing and improving the Work, but
#       excluding communication that is conspicuously marked or otherwise
#       designated in writing by the copyright owner as "Not a Contribution."
# 
#       "Contributor" shall mean Licensor and any individual or Legal Entity
#       on behalf of whom a Contribution has been received by Licensor and
#       subsequently incorporated within the Work.
# 
#    2. Grant of Copyright License. Subject to the terms and conditions of
#       this License, each Contributor hereby grants to You a perpetual,
#       worldwide, non-exclusive, no-charge, royalty-free, irrevocable
#       copyright license to reproduce, prepare Derivative Works of,
#       publicly display, publicly perform, sublicense, and distribute the
#       Work and such Derivative Works in Source or Object form.
# 
#    3. Grant of Patent License. Subject to the terms and conditions of
#       this License, each Contributor hereby grants to You a perpetual,
#       worldwide, non-exclusive, no-charge, royalty-free, irrevocable
#       (except as stated in this section) patent license to make, have made,
#       use, offer to sell, sell, import, and otherwise transfer the Work,
#       where such license applies only to those patent claims licensable
#       by such Contributor that are necessarily infringed by their
#       Contribution(s) alone or by combination of their Contribution(s)
#       with the Work to which such Contribution(s) was submitted. If You
#       institute patent litigation against any entity (including a
#       cross-claim or counterclaim in a lawsuit) alleging that the Work
#       or a Contribution incorporated within the Work constitutes direct
#       or contributory patent infringement, then any patent licenses
#       granted to You under this License for that Work shall terminate
#       as of the date such litigation is filed.
# 
#    4. Redistribution. You may reproduce and distribute copies of the
#       Work or Derivative Works thereof in any medium, with or without
#       modifications, and in Source or Object form, provided that You
#       meet the following conditions:
# 
#       (a) You must give any other recipients of the Work or
#           Derivative Works a copy of this License; and
# 
#       (b) You must cause any modified files to carry prominent notices
#           stating that You changed the files; and
# 
#       (c) You must retain, in the Source form of any Derivative Works
#           that You distribute, all copyright, patent, trademark, and
#           attribution notices from the Source form of the Work,
#           excluding those notices that do not pertain to any part of
#           the Derivative Works; and
# 
#       (d) If the Work includes a "NOTICE" text file as part of its
#           distribution, then any Derivative Works that You distribute must
#           include a readable copy of the attribution notices contained
#           within such NOTICE file, excluding those notices that do not
#           pertain to any part of the Derivative Works, in at least one
#           of the following places: within a NOTICE text file distributed
#           as part of the Derivative Works; within the Source form or
#           documentation, if provided along with the Derivative Works; or,
#           within a display generated by the Derivative Works, if and
#           wherever such third-party notices normally appear. The contents
#           of the NOTICE file are for informational purposes only and
#           do not modify the License. You may add Your own attribution
#           notices within Derivative Works that You distribute, alongside
#           or as an addendum to the NOTICE text from the Work, provided
#           that such additional attribution notices cannot be construed
#           as modifying the License.
# 
#       You may add Your own copyright statement to Your modifications and
#       may provide additional or different license terms and conditions
#       for use, reproduction, or distribution of Your modifications, or
#       for any such Derivative Works as a whole, provided Your use,
#       reproduction, and distribution of the Work otherwise complies with
#       the conditions stated in this License.
# 
#    5. Submission of Contributions. Unless You explicitly state otherwise,
#       any Contribution intentionally submitted for inclusion in the Work
#       by You to the Licensor shall be under the terms and conditions of
#       this License, without any additional terms or conditions.
#       Notwithstanding the above, nothing herein shall supersede or modify
#       the terms of any separate license agreement you may have executed
#       with Licensor regarding such Contributions.
# 
#    6. Trademarks. This License does not grant permission to use the trade
#       names, trademarks, service marks, or product names of the Licensor,
#       except as required for reasonable and customary use in describing the
#       origin of the Work and reproducing the content of the NOTICE file.
# 
#    7. Disclaimer of Warranty. Unless required by applicable law or
#       agreed to in writing, Licensor provides the Work (and each
#       Contributor provides its Contributions) on an "AS IS" BASIS,
#       WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
#       implied, including, without limitation, any warranties or conditions
#       of TITLE, NON-INFRINGEMENT, MERCHANTABILITY, or FITNESS FOR A
#       PARTICULAR PURPOSE. You are solely responsible for determining the
#       appropriateness of using or redistributing the Work and assume any
#       risks associated with Your exercise of permissions under this License.
# 
#    8. Limitation of Liability. In no event and under no legal theory,
#       whether in tort (including negligence), contract, or otherwise,
#       unless required by applicable law (such as deliberate and grossly
#       negligent acts) or agreed to in writing, shall any Contributor be
#       liable to You for damages, including any direct, indirect, special,
#       incidental, or consequential damages of any character arising as a
#       result of this License or out of the use or inability to use the
#       Work (including but not limited to damages for loss of goodwill,
#       work stoppage, computer failure or malfunction, or any and all
#       other commercial damages or losses), even if such Contributor
#       has been advised of the possibility of such damages.
# 
#    9. Accepting Warranty or Additional Liability. While redistributing
#       the Work or Derivative Works thereof, You may choose to offer,
#       and charge a fee for, acceptance of support, warranty, indemnity,
#       or other liability obligations and/or rights consistent with this
#       License. However, in accepting such obligations, You may act only
#       on Your own behalf and on Your sole responsibility, not on behalf
#       of any other Contributor, and only if You agree to indemnify,
#       defend, and hold each Contributor harmless for any liability
#       incurred by, or claims asserted against, such Contributor by reason
#       of your accepting any such warranty or additional liability.
# 
#    END OF TERMS AND CONDITIONS
# 
#    APPENDIX: How to apply the Apache License to your work.
# 
#       To apply the Apache License to your work, attach the following
#       boilerplate notice, with the fields enclosed by brackets "[]"
#       replaced with your own identifying information. (Don't include
#       the brackets!)  The text should be enclosed in the appropriate
#       comment syntax for the file format. We also recommend that a
#       file or class name and description of purpose be included on the
#       same "printed page" as the copyright notice for easier
#       identification within third-party archives.
# 
#    Copyright [yyyy] [name of copyright owner]
# 
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
# 
#        http://www.apache.org/licenses/LICENSE-2.0
# 
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.
"""Kaggriculture route-replay chassis (pure Python, stdlib only).

A *route* is a pre-computed tape of 719 Kaggle-format actions
``{"farmer": [op, ...], "hands": [[op, ...], ...], "market": [[order, item, qty], ...]}``.
The chassis replays the tape chosen by a caller-supplied ``router`` and wraps it
in small reactive layers (each independently switchable via ``settings``):

    hand_align            pad/truncate hands to the real hand count      (fieldbook_logic)
    weed_repair           DIG a weed that blocks PLANT/BUILD, replay      (tetsutani + task spec)
    sell_lead             sell next step's lots one step early            (fieldbook _lead_sale)
    front_run             sell before the opponent's scheduled SELL       (hook; opponent_plan)
    budget_guard          fund each 72-step block's purchases             (six_day_budget_guard.hpp)
    room_guard            keep shed <= 99 at hour 23                      (tetsutani)
    clamp_sells           trim SELL orders to the projected shed          (tetsutani)
    dead_stock            sell stock the route will never sell            (tetsutani)
    terminal_liquidation  step >= 718: sell the whole projected shed      (fieldbook _terminal_sale)

Engine facts (verified against kaggle_environments 1.32.7, env_1_32_7.py):
  observation["farms"][p] = {"money", "tiles"[y][x], "farmer"[x,y], "hands"[[x,y]..],
                             "unlocked_quadrants", "hires_today"}
  tiles: None (empty) | "LOCKED" | {"kind": WEED|COOP|PASTURE|PLANT, "crop"/"animal", ...}
  observation["private"] = {"shed": {item: n}, "seeds": {crop: n}, "inventories": [{}...]}
  observation["market"] = {"inventory": {...}, "prices": {...}}
  observation["town"] = {"unlocked_shops": [...]}
  Agents act on steps 0..718 (interpreter marks DONE once step >= episodeSteps-2).
"""
from __future__ import annotations

import copy

PRODUCTS = ("WHEAT", "CARROT", "TOMATO", "STRAWBERRY", "MELON", "EGG", "MILK", "WOOL", "FERTILIZER")
SEED_PRICE = {"WHEAT": 10, "CARROT": 20, "TOMATO": 50, "STRAWBERRY": 100, "MELON": 80}
ANIMAL_COST = {"GOOSE": 300, "COW": 400, "SHEEP": 500}
ANIMAL_STRUCTURE = {"GOOSE": "COOP", "COW": "PASTURE", "SHEEP": "PASTURE"}
LAND_PRICES = (1000, 2000, 4000)
MOVES = {"NORTH": (0, -1), "SOUTH": (0, 1), "EAST": (1, 0), "WEST": (-1, 0)}
FRONT_RUN_ITEMS = ("MILK", "WOOL", "STRAWBERRY", "MELON")
LAST_ACT_STEP = 718
PASS_ACTION = {"farmer": ["PASS"], "hands": [], "market": []}

DEFAULT_SETTINGS = {
    "hand_align": True,
    "weed_repair": True,
    "sell_lead": True,
    "front_run": True,
    "budget_guard": True,
    "room_guard": True,
    "clamp_sells": True,
    "dead_stock": True,
    "terminal_liquidation": True,
    # tunables
    "block_turns": 72,
    "shed_capacity": 100,
    "board_size": 10,
    "max_orders": 10,
    "turns_per_day": 24,
    "min_sell_price": 2,
}


# --------------------------------------------------------------------------- helpers
def _get(value, key, default=None):
    """Field access that works for dicts and Kaggle Struct/attribute objects."""
    if isinstance(value, dict):
        return value.get(key, default)
    getter = getattr(value, "get", None)
    if callable(getter):
        return getter(key, default)
    return getattr(value, key, default)


def _int(value, default=0):
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def _fib(n):
    a, b = 1, 1
    for _ in range(n):
        a, b = b, a + b
    return a


def _step_of(observation):
    raw = _get(observation, "step")
    if raw is not None:
        return _int(raw)
    return _int(_get(observation, "day", 0)) * 24 + _int(_get(observation, "hour", 0))


def _shed_adjacent(pos, board):
    if not isinstance(pos, (list, tuple)) or len(pos) < 2:
        return False
    half = board // 2
    return pos[0] in (half - 1, half) and pos[1] in (half - 1, half)


def _tile_at(tiles, pos):
    try:
        x, y = int(pos[0]), int(pos[1])
        return tiles[y][x]
    except (TypeError, ValueError, IndexError):
        return "LOCKED"


def _is_noop(act, tile, inv, seeds, pos, board):
    """True when the engine will certainly ignore ``act`` (mirrors _apply_unit_action)."""
    if not act:
        return True
    op = act[0]
    x, y = pos[0], pos[1]
    if op in MOVES:
        dx, dy = MOVES[op]
        return not (0 <= x + dx < board and 0 <= y + dy < board)
    if op == "PASS":
        return True
    adjacent = _shed_adjacent(pos, board)
    if op == "DROP":
        return (not adjacent) or (not inv)
    if op == "PICKUP":
        return not adjacent
    if op == "PLACE":
        item = act[1] if len(act) > 1 else None
        if item in ANIMAL_STRUCTURE and isinstance(tile, dict) \
                and _get(tile, "kind") == ANIMAL_STRUCTURE[item] and _get(tile, "animal") is None:
            return _int(_get(inv, item, 0)) <= 0
        return (not adjacent) or _int(_get(inv, item, 0)) <= 0
    if tile == "LOCKED":
        return True
    is_dict = isinstance(tile, dict)
    kind = _get(tile, "kind") if is_dict else None
    animal = is_dict and _get(tile, "animal") is not None
    if op == "PLANT":
        return tile is not None or _int(_get(seeds, act[1] if len(act) > 1 else None, 0)) <= 0
    if op == "WATER":
        return kind != "PLANT" or bool(_get(tile, "watered_today"))
    if op == "HARVEST":
        return (not is_dict) or _int(_get(tile, "yield_units", 0)) <= 0
    if op == "FERTILIZE":
        return kind != "PLANT" or _int(_get(inv, "FERTILIZER", 0)) <= 0
    if op == "DIG":
        return tile is None or animal
    if op in ("BUILD_COOP", "BUILD_PASTURE"):
        return tile is not None
    if op == "FEED":
        return (not animal) or bool(_get(tile, "fed_today")) or _int(_get(inv, "WHEAT", 0)) <= 0
    if op == "COLLECT_FERTILIZER":
        return (not animal) or (not _get(tile, "fertilizer_available"))
    if op == "CARE":
        return (not animal) or bool(_get(tile, "cared_today"))
    return True


class _View:
    """Cheap per-step snapshot of everything the layers read from the observation."""

    def __init__(self, observation, player, cfg):
        farms = list(_get(observation, "farms", []) or [])
        self.farm = farms[player] if player < len(farms) else {}
        self.rival = farms[1 - player] if len(farms) >= 2 and 1 - player < len(farms) else {}
        private = _get(observation, "private", {}) or {}
        self.shed = {k: max(0, _int(v)) for k, v in dict(_get(private, "shed", {}) or {}).items()}
        self.seeds = dict(_get(private, "seeds", {}) or {})
        self.invs = [dict(i or {}) for i in (_get(private, "inventories", []) or [])]
        market = _get(observation, "market", {}) or {}
        self.prices = {k: _int(v) for k, v in dict(_get(market, "prices", {}) or {}).items()}
        self.money = float(_get(self.farm, "money", 0.0) or 0.0)
        self.tiles = _get(self.farm, "tiles", []) or []
        self.board = len(self.tiles) or cfg["board_size"]
        self.positions = [_get(self.farm, "farmer", None)] + [list(p) for p in (_get(self.farm, "hands", []) or [])]
        self.hires_today = _int(_get(self.farm, "hires_today", 0))
        self.quadrants = len(list(_get(self.farm, "unlocked_quadrants", []) or []))

    def inv(self, idx):
        return self.invs[idx] if idx < len(self.invs) else {}

    def in_hands(self, item):
        return sum(max(0, _int(_get(inv, item, 0))) for inv in self.invs)


# --------------------------------------------------------------------------- chassis
class Chassis:
    """Replays ``routes[router(...)]`` with reactive safety/market layers.

    routes         : {route_id: list of >= 719 Kaggle action dicts}
    router         : callable(observation, step, state_dict) -> route_id, called every
                     step; ``state_dict`` is per-player and persists across the game.
    settings       : overrides for DEFAULT_SETTINGS (layer switches + tunables)
    opponent_plan  : optional list of the opponent's expected actions (front_run hook)
    """

    def __init__(self, routes, router=None, settings=None, opponent_plan=None):
        self.routes = {rid: list(tape) for rid, tape in routes.items()}
        self.router = router or (lambda observation, step, state: next(iter(self.routes)))
        self.cfg = dict(DEFAULT_SETTINGS)
        self.cfg.update(settings or {})
        self.opponent_plan = opponent_plan
        self.players = {}
        self.diagnostics = {"layer_fallbacks": 0, "entry_fallbacks": 0}
        self._future_sells = {}   # route id -> {item: [remaining planned SELL qty from step t]}

    # ---- state -----------------------------------------------------------------
    def _state(self, player, step):
        st = self.players.get(player)
        if st is None or step == 0 or step <= st["last_step"]:
            st = {"last_step": -1, "route": None, "router_state": {},
                  "pending": {}, "sell_state": {"due_step": -1, "suppress": {}}}
            self.players[player] = st
        st["last_step"] = step
        return st

    def _route_action(self, route, step):
        tape = self.routes[route]
        if 0 <= step < len(tape) and isinstance(tape[step], dict):
            return copy.deepcopy(tape[step])
        return copy.deepcopy(PASS_ACTION)

    def future_sells(self, route, item, step):
        """Planned SELL quantity of ``item`` in route steps >= ``step`` (suffix sums)."""
        table = self._future_sells.get(route)
        if table is None:
            tape = self.routes[route]
            n = len(tape)
            table = {p: [0] * (n + 1) for p in PRODUCTS}
            for t in range(n - 1, -1, -1):
                for p in PRODUCTS:
                    table[p][t] = table[p][t + 1]
                for o in (tape[t].get("market") or []) if isinstance(tape[t], dict) else []:
                    if o and o[0] == "SELL" and len(o) >= 3 and o[1] in table:
                        table[o[1]][t] += max(0, _int(o[2]))
            self._future_sells[route] = table
        col = table.get(item)
        return col[step] if col and 0 <= step < len(col) else 0

    # ---- main entry -----------------------------------------------------------
    def act(self, observation, configuration=None):
        if len(_get(observation, "farms", []) or []) < 2:
            raise ValueError("incomplete observation")  # factory falls back to tape
        step = _step_of(observation)
        player = _int(_get(observation, "player", 0))
        st = self._state(player, step)
        cfg = self.cfg
        view = _View(observation, player, cfg)

        route = self.router(observation, step, st["router_state"])
        if route not in self.routes:
            route = st["route"] if st["route"] in self.routes else next(iter(self.routes))
        st["route"] = route
        action = self._route_action(route, step)
        raw = copy.deepcopy(action)
        try:
            if cfg["hand_align"]:
                self._hand_align(action, view)
            if cfg["weed_repair"]:
                self._weed_repair(action, view, st, route, step)
            if cfg["sell_lead"] or cfg["front_run"]:
                self._apply_suppression(action, st["sell_state"], step)
            projected = self._projected_shed(action, view)
            lead_available = dict(projected)
            next_sup = {"due_step": -1, "suppress": {}, "r36_debts": st["sell_state"].get("r36_debts", {})}
            if cfg["sell_lead"]:
                self._sell_lead(action, view, lead_available, route, step, next_sup)
            if cfg["front_run"] and self.opponent_plan:
                self._front_run(action, view, lead_available, route, step, next_sup)
            st["sell_state"] = next_sup
            if cfg["budget_guard"]:
                self._budget_guard(action, view, route, step)
            if cfg["room_guard"]:
                self._room_guard(action, view, route, step)
            if cfg["clamp_sells"]:
                self._clamp_sells(action, projected)
            if cfg["dead_stock"]:
                self._dead_stock(action, view, projected, route, step)
            if cfg["terminal_liquidation"]:
                self._terminal_liquidation(action, projected, step)
            action["market"] = action["market"][: cfg["max_orders"]]
            return action
        except Exception:
            self.diagnostics["layer_fallbacks"] += 1
            return raw

    # ---- layer: hand_align ----------------------------------------------------
    def _hand_align(self, action, view):
        """Pad with PASS / truncate the tape's hand list to the real number of hands
        (fieldbook_logic.act). Extra hands would be ignored by the engine anyway;
        missing ones just idle, so alignment only tidies the action."""
        expected = max(0, len(view.positions) - 1)
        hands = list(action.get("hands") or [])
        hands.extend([["PASS"] for _ in range(max(0, expected - len(hands)))])
        action["hands"] = hands[:expected]

    # ---- layer: weed_repair ---------------------------------------------------
    def _weed_repair(self, action, view, st, route, step):
        """If a PLANT/BUILD_* target tile is a WEED, DIG now and queue the intended
        action for that unit; the queue replays on a later step when the unit still
        stands there and its tape action would be a no-op (the displaced no-op is
        queued behind it, so PLANT -> WATER chains survive). A PLANT is only replayed
        when the unit's next tape action is not a move, so the mandatory same-day
        WATER can follow; otherwise the seed is kept. A no-op turn spent on a weed
        is also converted to DIG (tetsutani weed_dig)."""
        units = [action.get("farmer") or ["PASS"]] + list(action.get("hands") or [])
        pending = st["pending"]
        tape = self.routes[route]
        nxt = tape[step + 1] if step + 1 < len(tape) and isinstance(tape[step + 1], dict) else {}
        next_units = [nxt.get("farmer") or ["PASS"]] + list(nxt.get("hands") or [])
        for i in range(min(len(units), len(view.positions))):
            pos = view.positions[i]
            if not isinstance(pos, (list, tuple)):
                continue
            pos = (int(pos[0]), int(pos[1]))
            tile = _tile_at(view.tiles, pos)
            act = list(units[i])
            queue = pending.get(i)
            if queue and queue[0][0] != pos:
                pending.pop(i, None)
                queue = None
            is_weed = isinstance(tile, dict) and _get(tile, "kind") == "WEED"
            noop = _is_noop(act, tile, view.inv(i), view.seeds, pos, view.board)
            next_op = next_units[i][0] if i < len(next_units) and next_units[i] else "PASS"
            if act and act[0] in ("PLANT", "BUILD_COOP", "BUILD_PASTURE") and is_weed:
                pending.setdefault(i, []).append((pos, act))
                act = ["DIG"]
            elif queue and noop:
                _, replay = queue[0]
                if replay[0] == "PLANT" and next_op in MOVES:
                    pending.pop(i, None)          # WATER could never follow: keep the seed
                else:
                    queue.pop(0)
                    if act and act[0] != "PASS" and act[0] not in MOVES:
                        queue.append((pos, act))
                    act = replay
                    if not queue:
                        pending.pop(i, None)
            elif is_weed and noop:
                act = ["DIG"]
            units[i] = act
        action["farmer"] = units[0]
        action["hands"] = units[1:]

    # ---- projected shed -------------------------------------------------------
    def _projected_shed(self, action, view):
        """Shed contents after this step's unit actions but before the market runs:
        PICKUP removes, DROP/PLACE(non-animal) near the shed adds up to capacity
        (fieldbook _projected_shed / tetsutani projected shed)."""
        cap = self.cfg["shed_capacity"]
        proj = {p: view.shed.get(p, 0) for p in PRODUCTS}
        for k, v in view.shed.items():
            proj.setdefault(k, v)
        total = sum(proj.values())
        units = [action.get("farmer") or ["PASS"]] + list(action.get("hands") or [])
        for i in range(min(len(units), len(view.positions))):
            if not _shed_adjacent(view.positions[i], view.board):
                continue
            act = units[i]
            op = act[0] if act else "PASS"
            inv = view.inv(i)
            if op == "PICKUP" and len(act) >= 2 and act[1] in proj:
                qty = min(proj[act[1]], max(0, _int(act[2]) if len(act) >= 3 else 1))
                proj[act[1]] -= qty
                total -= qty
            elif op == "DROP":
                for item, held in inv.items():
                    take = min(max(0, _int(held)), max(0, cap - total))
                    if take > 0:
                        proj[item] = proj.get(item, 0) + take
                        total += take
            elif op == "PLACE" and len(act) >= 2 and act[1] not in ANIMAL_STRUCTURE:
                item = act[1]
                take = min(max(0, _int(act[2]) if len(act) >= 3 else 1),
                           max(0, _int(_get(inv, item, 0))), max(0, cap - total))
                if take > 0:
                    proj[item] = proj.get(item, 0) + take
                    total += take
        return proj

    # ---- layer: sell_lead / front_run suppression ------------------------------
    @staticmethod
    def _apply_suppression(action, sell_state, step):
        """Remove from this step's SELLs the quantities already sold a step early."""
        if sell_state.get("due_step") != step:
            return
        remaining = dict(sell_state.get("suppress", {}))
        kept = []
        for order in action.get("market") or []:
            order = list(order)
            if order and order[0] == "SELL" and len(order) >= 3 and remaining.get(order[1], 0) > 0:
                removed = min(max(0, _int(order[2])), remaining[order[1]])
                order[2] = _int(order[2]) - removed
                remaining[order[1]] -= removed
                # A zero-quantity order keeps later market race slots intact.
            kept.append(order)
        action["market"] = kept

    @staticmethod
    def _add_sell(action, item, qty, max_orders, merge=True):
        market = action.setdefault("market", [])
        if merge:
            for order in market:
                if order and order[0] == "SELL" and order[1] == item:
                    order[2] = _int(order[2]) + qty
                    return True
        if len(market) >= max_orders:
            return False
        market.append(["SELL", item, qty])
        return True

    def _sell_lead(self, action, view, projected, route, step, next_sup):
        """fieldbook _lead_sale: when step % 4 != 0 (no town consumption between the
        two steps) sell the lots the tape plans to SELL next step now, for products
        other than WHEAT/FERTILIZER we already hold, and suppress them next step.
        Skipped at the last step, at shop-unlock boundaries and if a SELL for that
        product is already queued this step."""
        cfg = self.cfg
        nxt = step + 1
        unlock_period = 3 * cfg["turns_per_day"]
        if nxt > LAST_ACT_STEP or nxt % unlock_period == 0 or step % 4 == 0:
            return
        tape = self.routes[route]
        future = tape[nxt] if nxt < len(tape) and isinstance(tape[nxt], dict) else {}
        planned = {}
        for o in future.get("market") or []:
            if o and o[0] == "SELL" and len(o) >= 3 and o[1] in PRODUCTS:
                planned[o[1]] = planned.get(o[1], 0) + max(0, _int(o[2]))
        already = {o[1] for o in action.get("market") or [] if o and o[0] == "SELL" and len(o) > 1}
        for item in PRODUCTS:
            if item in ("WHEAT", "FERTILIZER") or planned.get(item, 0) <= 0 or item in already:
                continue
            qty = min(projected.get(item, 0), planned[item])
            if qty <= 0 or view.prices.get(item, 0) < cfg["min_sell_price"]:
                continue
            if not self._add_sell(action, item, qty, cfg["max_orders"], merge=False):
                break
            projected[item] -= qty
            next_sup["suppress"][item] = next_sup["suppress"].get(item, 0) + qty
        if next_sup["suppress"]:
            next_sup["due_step"] = nxt

    def _front_run(self, action, view, projected, route, step, next_sup):
        """Hook: if ``opponent_plan`` (their expected tape) schedules a SELL of
        MILK/WOOL/STRAWBERRY/MELON next step, sell what we hold of it now (before
        their supply depresses the price) and suppress our own SELL of that quantity
        next step. Bounded by our own remaining planned sales so it never dumps."""
        cfg = self.cfg
        nxt = step + 1
        plan = self.opponent_plan
        if nxt > LAST_ACT_STEP or nxt >= len(plan) or not isinstance(plan[nxt], dict):
            return
        already = {o[1] for o in action.get("market") or [] if o and o[0] == "SELL" and len(o) > 1}
        for o in plan[nxt].get("market") or []:
            if not (o and o[0] == "SELL" and len(o) >= 3 and o[1] in FRONT_RUN_ITEMS):
                continue
            item = o[1]
            if item in already or view.prices.get(item, 0) < cfg["min_sell_price"]:
                continue
            own_next = sum(max(0, _int(x[2])) for x in self.routes[route][nxt].get("market", [])
                           if len(x) >= 3 and x[0] == "SELL" and x[1] == item)
            qty = min(projected.get(item, 0), max(0, _int(o[2])), own_next)
            if qty <= 0:
                continue
            if not self._add_sell(action, item, qty, cfg["max_orders"], merge=False):
                break
            projected[item] -= qty
            already.add(item)
            next_sup["suppress"][item] = next_sup["suppress"].get(item, 0) + qty
        if next_sup["suppress"]:
            next_sup["due_step"] = nxt

    # ---- layer: budget_guard --------------------------------------------------
    def _block_requirements(self, view, route, start, end):
        """Planned purchase cost and item reserves for tape steps [start, end)
        (six_day_budget_guard.hpp calculate_six_day_requirements)."""
        tape = self.routes[route]
        budget = 0.0
        seed_bal, item_bal = {}, {}
        seed_need, item_need = {}, {}
        hires_by_day = {}
        quadrants = view.quadrants
        for t in range(start, min(end, len(tape))):
            a = tape[t] if isinstance(tape[t], dict) else {}
            for u in [a.get("farmer") or ["PASS"]] + list(a.get("hands") or []):
                if not u:
                    continue
                op = u[0]
                arg = u[1] if len(u) > 1 else None
                qty = max(1, _int(u[2]) if len(u) > 2 else 1)
                if op == "PLANT" and arg in SEED_PRICE:
                    seed_bal[arg] = seed_bal.get(arg, 0) - 1
                    seed_need[arg] = max(seed_need.get(arg, 0), -seed_bal[arg])
                elif op == "FEED":
                    item_bal["WHEAT"] = item_bal.get("WHEAT", 0) - 1
                    item_need["WHEAT"] = max(item_need.get("WHEAT", 0), -item_bal["WHEAT"])
                elif op == "FERTILIZE":
                    item_bal["FERTILIZER"] = item_bal.get("FERTILIZER", 0) - 1
                    item_need["FERTILIZER"] = max(item_need.get("FERTILIZER", 0), -item_bal["FERTILIZER"])
                elif op == "PLACE" and arg is not None:
                    item_bal[arg] = item_bal.get(arg, 0) - qty
                    item_need[arg] = max(item_need.get(arg, 0), -item_bal[arg])
            for o in a.get("market") or []:
                if not o:
                    continue
                op = o[0]
                item = o[1] if len(o) > 1 else None
                qty = max(1, _int(o[2]) if len(o) > 2 else 1)
                if op == "HIRE":
                    day = (t - start) // self.cfg["turns_per_day"]
                    hires_by_day[day] = hires_by_day.get(day, 0) + 1
                elif op == "BUY_LAND":
                    extra = quadrants - 1
                    if 0 <= extra < len(LAND_PRICES):
                        budget += LAND_PRICES[extra]
                        quadrants += 1
                elif op == "BUY_SEED" and item in SEED_PRICE:
                    budget += SEED_PRICE[item] * qty
                    seed_bal[item] = seed_bal.get(item, 0) + qty
                elif op == "BUY_PRODUCT" and item in ("WHEAT", "FERTILIZER"):
                    budget += view.prices.get(item, 0) * qty
                    item_bal[item] = item_bal.get(item, 0) + qty
                elif op == "BUY_ANIMAL" and item in ANIMAL_COST:
                    budget += ANIMAL_COST[item] * qty
                    item_bal[item] = item_bal.get(item, 0) + qty
        for day, n in hires_by_day.items():
            first = view.hires_today if day == 0 else 0
            for k in range(n):
                budget += _fib(first + k)
        return budget, item_need

    def _budget_guard(self, action, view, route, step):
        """At every block boundary (step % 72 == 0) make sure cash + the value of
        stock the block already plans to sell covers the block's purchases (hires,
        land, seeds, animals, products). A shortfall is covered by extra SELLs of
        unprotected shed stock, highest price first; SELLs are moved in front of
        the buys so the money is there when they execute."""
        cfg = self.cfg
        block = cfg["block_turns"]
        if block <= 0 or step % block != 0:
            return
        budget, item_need = self._block_requirements(view, route, step, step + block)
        market = action.setdefault("market", [])
        existing = {}
        for o in market:
            if o and o[0] == "SELL" and len(o) >= 3:
                existing[o[1]] = existing.get(o[1], 0) + max(0, _int(o[2]))
        cash = view.money
        for item in PRODUCTS:
            planned = max(existing.get(item, 0), self.future_sells(route, item, step)
                          - self.future_sells(route, item, step + block))
            cash += min(view.shed.get(item, 0), planned) * view.prices.get(item, 0)
        shortfall = budget - cash
        if shortfall <= 0:
            return
        candidates = []
        for item in PRODUCTS:
            price = view.prices.get(item, 0)
            if price < cfg["min_sell_price"]:
                continue
            protected = max(0, item_need.get(item, 0) - view.in_hands(item))
            avail = view.shed.get(item, 0) - protected - existing.get(item, 0)
            if avail > 0:
                candidates.append((-price, item, avail, price))
        candidates.sort()
        added = False
        for _, item, avail, price in candidates:
            if shortfall <= 0:
                break
            qty = min(avail, -(-int(shortfall) // price))
            if self._add_sell(action, item, qty, cfg["max_orders"]):
                shortfall -= qty * price
                added = True
        if added:
            sells = [o for o in market if o and o[0] == "SELL"]
            others = [o for o in market if not (o and o[0] == "SELL")]
            action["market"] = sells + others

    # ---- layer: room_guard ----------------------------------------------------
    def _room_guard(self, action, view, route, step):
        """tetsutani room_guard: at hour 23 the end-of-day drop pushes every unit's
        inventory into the shed and overflow is destroyed. Estimate the shed after
        this step (stock + carried + harvest/collect - feed/fertilize/place + buys -
        sells) and, if it exceeds capacity-1, add SELLs preferring products with no
        future planned sale, then highest price."""
        cfg = self.cfg
        if step % cfg["turns_per_day"] != cfg["turns_per_day"] - 1:
            return
        cap = cfg["shed_capacity"]
        units = [action.get("farmer") or ["PASS"]] + list(action.get("hands") or [])
        carried = sum(max(0, _int(n)) for inv in view.invs for n in inv.values())
        produced = consumed = 0
        for i in range(min(len(units), len(view.positions))):
            tile = _tile_at(view.tiles, view.positions[i])
            a = units[i]
            if not a:
                continue
            op = a[0]
            if op == "HARVEST" and isinstance(tile, dict):
                produced += max(0, _int(_get(tile, "yield_units", 0)))
            elif op == "COLLECT_FERTILIZER" and isinstance(tile, dict) and _get(tile, "fertilizer_available"):
                produced += 1
            elif op in ("FEED", "FERTILIZE"):
                consumed += 1
            elif op == "PLACE" and len(a) > 1 and a[1] in ANIMAL_STRUCTURE:
                consumed += 1
        market = action.setdefault("market", [])
        planned_sells, planned_buys = {}, 0
        for o in market:
            if not o:
                continue
            if o[0] == "SELL" and len(o) >= 3:
                planned_sells[o[1]] = planned_sells.get(o[1], 0) + max(0, _int(o[2]))
            elif o[0] in ("BUY_PRODUCT", "BUY_ANIMAL") and len(o) >= 3:
                planned_buys += max(0, _int(o[2]))
        shed_total = sum(view.shed.values())
        fillable = sum(min(view.shed.get(it, 0), n) for it, n in planned_sells.items())
        needed = shed_total + carried + produced - consumed + planned_buys - fillable - (cap - 1)
        if needed <= 0:
            return
        priority = sorted(PRODUCTS, key=lambda it: (self.future_sells(route, it, step + 1) > 0,
                                                   -view.prices.get(it, 0), it))
        for item in priority:
            avail = max(0, view.shed.get(item, 0) - planned_sells.get(item, 0))
            qty = min(needed, avail)
            if qty <= 0 or view.prices.get(item, 0) < 1:
                continue
            if not self._add_sell(action, item, qty, cfg["max_orders"]):
                continue
            planned_sells[item] = planned_sells.get(item, 0) + qty
            needed -= qty
            if needed <= 0:
                break

    # ---- layer: clamp_sells ---------------------------------------------------
    @staticmethod
    def _clamp_sells(action, projected):
        """Clamp against a sequential stock upper bound, retaining market slots.

        Earlier BUY_PRODUCT orders can fund a wheat wash's sell leg. Their full
        quantity is an upper bound; the engine enforces actual cash/capacity.
        Removing empty orders would change the later lockstep market races.
        """
        avail = dict(projected)
        kept = []
        for o in action.get("market") or []:
            if o and o[0] == "SELL" and len(o) >= 3:
                have = avail.get(o[1], 0)
                n = min(_int(o[2]), have)
                n = max(0, n)
                avail[o[1]] = have - n
                kept.append(["SELL", o[1], n])
            else:
                kept.append(o)
                if o and o[0] in ("BUY_PRODUCT", "BUY_ANIMAL") and len(o) >= 3:
                    avail[o[1]] = avail.get(o[1], 0) + max(0, _int(o[2]))
        action["market"] = kept

    # ---- layer: dead_stock ----------------------------------------------------
    def _dead_stock(self, action, view, projected, route, step):
        """tetsutani dead_stock: stock beyond everything the rest of the route still
        plans to SELL is dead; sell it now when price > 1 (on day 29 everything not
        already in this step's orders is dead). Highest value lots first."""
        planned = {}
        for o in action.get("market") or []:
            if o and o[0] == "SELL" and len(o) >= 3:
                planned[o[1]] = planned.get(o[1], 0) + _int(o[2])
        day = step // self.cfg["turns_per_day"]
        extra = []
        for item in PRODUCTS:
            have = projected.get(item, 0) - planned.get(item, 0)
            if have <= 0:
                continue
            surplus = have if day >= 29 else have - self.future_sells(route, item, step + 1)
            if surplus > 0 and view.prices.get(item, 0) > 1:
                extra.append(["SELL", item, surplus])
        extra.sort(key=lambda o: -view.prices.get(o[1], 0) * o[2])
        action["market"] = (action.get("market") or []) + extra

    # ---- layer: terminal_liquidation -----------------------------------------
    def _terminal_liquidation(self, action, projected, step):
        """fieldbook _terminal_sale: on the final acting step (>= 718) replace the
        market orders with a SELL of the whole projected shed."""
        if step < LAST_ACT_STEP:
            return
        action["market"] = [["SELL", item, qty] for item, qty in projected.items()
                            if qty > 0 and item in PRODUCTS][: self.cfg["max_orders"]]


# --------------------------------------------------------------------------- factory
def make_agent(routes, router=None, opponent_plan=None, **settings):
    """Build a Kaggle ``agent(observation, configuration)`` closure that never raises:
    a failure inside a layer falls back to the raw tape action, and a failure even
    before that falls back to PASS (with hands padded when possible)."""
    chassis = Chassis(routes, router, settings, opponent_plan)

    def agent(observation, configuration=None):
        try:
            return chassis.act(observation, configuration)
        except Exception:
            chassis.diagnostics["entry_fallbacks"] += 1
            try:
                step = _step_of(observation)
                player = _int(_get(observation, "player", 0))
                tape = chassis.routes.get(chassis.players.get(player, {}).get("route"),
                                          next(iter(chassis.routes.values())))
                if 0 <= step < len(tape):
                    return copy.deepcopy(tape[step])
            except Exception:
                pass
            try:
                farms = _get(observation, "farms", []) or []
                hands = _get(farms[_int(_get(observation, "player", 0))], "hands", []) or []
                return {"farmer": ["PASS"], "hands": [["PASS"] for _ in hands], "market": []}
            except Exception:
                return copy.deepcopy(PASS_ACTION)

    agent.chassis = chassis
    return agent

# Extracted from the frozen One More Wheat source on 2026-09-22.
# Upstream Apache-2.0 notices are retained above. Generic library only.

# Standalone observation-guarded reconstruction of a public production plan.
import base64,json,zlib
_SCHEDULE=json.loads(zlib.decompress(base64.b85decode('c-rM%U5{H=a{MpzJP#H*8aa8BC9W;3>@oDQ#KsT|1G|d=!REoqTaf=ASu-RrPghq}_dOiR@skLSc<=c>-PP6AKmE_uKYsc3pMU@L>R*4l`tkYOw^tvoum1g)|NPs3ef;9%$AA9v>wo<HzdwHd>FS&JfBpIS53jy|{`%_r>c!pu>iWrt>-(>Nd~^5m{fl=Wzu$kid;am?r-#2BfAIFZ-R{T5PYQqd@W0n*t$g+3&+mU+v>|El+uiHerxtyB{&%n5?5@Ozq?`ADADZ&b`&X}D{`_&+-o5|y>tjn6tz7nxe|dVD_5XNp$3c7j{KXE9*-uwL+`W1C-KVajPy5~5cgwHj7{m3DPvXOW*q$}%_|oz1*Ky2~mU+#1@qC=O`1r%nE$8CY9P-!Lptrl-%a8x}``zoiAFi%9{%}2v!*YFr_dfInjo<wT-J;>WfBNmuXYY;gh$9Ba@P~KD_nft3c;oK**weRn@58DbmopxZ{quLbH>B6uXdm7KH_6bI!e%kv9LM`KgZG_Tz9ly0@Xh`6>+^jW>+^+{_IG&Qc`KWPAD8;+ne=_;Qa>Iz^1X|BojLaY+{br>*V`k1eo}ArL3nx|8i#Ssmxp__HF)3RHL!NH$@|G{hvA;^-uP^DgINRbbllosr(<~9ix-bPHR1k$Ek8`3Y4DEl0nBgXxu+fue_Q$7>;rl1i@VpacQ4-k{HNWUcduT*`nONxotVy<d7K!Pi%0slC21<Xf9Zpc=iJbw#Lfz*5+5Ybu+mp5d<)-U!$V)bx%)BOOZ@3<;SDzVCV9bwiG~k?()b(p=0i^xA5j04p<@{Sp!dm__x+dM-uT@%7d(1#tFK2R{`ld3bjy#9^979IIEcoQk=9w}?2rW>AM()tv+eWgxuvI!KfXRZm~FPfwnNALv32rrKir?_DW`dmPl;Y;{UJ`r{9B84>=IY%ALk(zd!PxW%{Ll~h6L~>39^)2oW7Y+G$z1NdHhhY1tMaSbR_%w{0?xTzJf(^G#J)cahnf?bC|wSoA&Y1(G0PWhxRRIJM_@v81ZZ4P>mq;scBPs3O1bARo!?9)HE7R&9LKRzI*=WFP(<-rvpFx^w;AnQv>boyEo7G-|XJJ`KveI%T54qH9`W57c^S|`VW9&(3WAai`GI!iVv?iE^uaH4{tb)8$5TS=@ur|FrAiTE#7lH=;DOdk=HnS$H!+jY5#4}h{+y(k(aS|1Qd)wP}<u+%^H}$$^r5P07K_Sz_V3`V6+(iz=q%Ht4Fl_j&Em{-(%Z(Pg-^!vMx-k$#|g$Lg_18--zH&0yiPJN>&+!pdrj4L?(*9-MHa)=-O#Uk0+zVQfTNddQ{7+QlmXqtB>m<9QM;}C1fkcTRDyuhh&@PV>I0M!I~VGOK&8g!4-`<Feay|u)(;@@Ivv&EW|U-M2C$MJ(ZU|uuo18gigV68s)R$RD}@g(47X@DQ62ffgLo|haPLqCz0>)Sby|sT=(~29?k#^!A8wVZ6$()1!%Y?<riRFvcY&PGjnaElcRhDHkfI60!j=Whk84JF#zC51|fHVlZZ@a-O8b>d5C2+0WA9z42I!6#=(f@DZ<JsFX0?R3h#^%v_X8WMVw*O8?1f!|H`b4rg;<>{Bc|&YBhJHqV;>a{mGCl8<Zfr7Z@jCD<1~z*lN(gdAKh$3r}wZjfg;?0gefyFgktk!>Y(MK}$PCFvJ{6+S#R=i9sWXtb+ruGN>C<g4oOX3sN+l8N-n_WJ9plGX7jqc?QO&M4p@Vuq?IQ9vhd<*nN+S%El~*a2-s7X^(q&L>=qFc%IJ#-hJBM@t2z8=TPVI(4~LKy`>cd$EOa`nxC!X_0d@JCeM+?L^ZNYJH-v6%4=A13?UapYNO752+uuj6})K?_Sf|7;>*FL$h**_luDmYz6i`pM!hJ(Z*f)x&BJeUgv!hu$W<WR=@S4C8czo3M+}EeYB8WQOkpWDjJ)4j+C|uh9wyR&O?_jJ1NEu7x6J^yorK|PM*EqsW&)|=5?F;ep8UFk@v!Vfu|X%({_gJMKeq?-;-k0r@~VOk0+;&O7Yd$^CzR8=BZT+u-QC-r0xr6LE1LAjHN0%p;`%$BKXF+2!QI1dGI|o&11Ced<UAx%Hn1WdbF#}3oqL4s#a)Q11Ij3z;wht+<=e#0XWr1MNx(N*ws#Cx;|Zei2Qw{coT*Waz?s14;_4&vbk*a*hJ=^6^ZYrPbiyF#Cgy$@*5IjA=_+5?FaFBB&|JsW3T?%BfQBW3*E>3ABP++;c<dkr`$;avbTxx58P~ugu2Om8q#6z&p<!5;aB<ICqMHlu(=!%(Sc1^JrHdB+BDV?0$nb?TM!`Zqf%I~r+u5%o$lJd{*dj%)|FBBU7?w_>&5X3O_fh$T;e9B~238m708Jj4bcCa!Rd;nnkdI9sg_`ciYZ?nuHHd4KM7Uu|Pdgu@dX9ljOUsyj!J*FZocMocBzu5m$COB@ZpmemS^*4&#9GAuzbJB*unv9L?9n2Csrp^GeQtHM5J1#*T3jMR!W9N}Yb|=XY~#SRS`iew^_#BX4aK-aP8E#ecDZRxuC3;SAIEpRE)CMotsj7kOE=PnfSyA=tz_f3i3d-)otn?<RuAU7SSH(7sZ|^aizgC}CG64>k;(1cZEEL&J+xZ*<*5$O#@MeluiXsfGzV5q%=(lc)P)dkm5dycQa^~XBvj2-cpKhrfiQb|iHt#$*mjX@4Z1i(fX7*>XjHhUgtwuab3E9}4FWh|MJws9G*;hb1%uUO2JPEq=K!08(+#+LgOOg$K_aeC>=l9so%y86Pav`YI#(nnG2Sv5L(o@w09tuJ0H-aG5<$FJ4*t!>qu9U+NuoQ>oxe>kLGI5Gi{SfLumAjDnZoAF$fY3vNqmfk<;VV6Ms_)jM_i3eQKd`+m71u|$p9K^-gNp@-Vtc39Z-f;07vK#Fw!9cxNgkTCNiJF)~8Y<E$74;_Qn1^_2#<NwUbREmNJU`5nI(mhGnpfh`WR154B=6aIaIf_FTc2t#a7~MiPu5HKh^cd2<~mux`0H{^OYg(%V4B6OYwRn3KA8zP*8KO4wi+W=N)G6GnYm5h<h8PsXDwue-+VsFNOTcK|=7;kZ;@T*oZDPT5-tc%@A79ELnX*pBGr&+4Fu+h7!ntvq@jmNjPT0Vl>K&0CZ-Jdx@z2gazAh(o!BL(8b!Fn|5Ti#}p}F1enaTPjHHSK*O{D0OrAJ>Nf$3i<%Z=PI8y>AK?D22QaPhWhZzA9P5;e{064!I=l9mB#%&c?e(IkBTG!?u5)nz`twY_+J1T!*dFh$HpTtzGvMCBp0HwB2^)$zDj4hmSM|((M)ZiQARth!91=B#r$Sg+%yK1(+P^%5vHUNky{&jBmE2CG>@sXXRPDk!-LRBPWqbYF%`0MnGoQ~YqS+<*x#p27D=mJ&IMu=2#mT!AUDCsM}#dv9z*IFa%%}$`)IrMY>A;!OTuID@FZwQ<I9@W-l+>m*rRa=Wu1*%tgv%hc0F9?fu)=n$kFvSlYuVE;BYl1fT_q+UTn|4>vpj?EZ?Pk=YoecH!f)5u$K9bi+mF5$~QMCSmvDG9hUiEMGk+B_g?PpbXdzM#E(ow!-u{ux$c%&!|DV|lN+8&z2Ni3r_$UM#Oz|3G5&!&?W6h8D~&~;9FsPf&dl&li4S$$1yIQ=&mz0lxwPzxE(kzH2qz){U~w_tm`qkDRCP)Np`|y`f72Suc}oBQ!sDE)gdFx&s><!f!4XF5Iy?Ivrpis>-sN}*2S%Q3*q;hSr|5{AGQBbV1)vXoL25Lv^sZ$kns(TfCe(s$FY=I_Vc@tvD^$dIb!35+bk5+(45*Q?VPH@V9S{wc63nYuCr!D5xG<C<xPceReXjOxVH0u|6XkS(yGL~l_`jr1m2-ydQdI#|r_-m>5Ch6CQs8^%0Iwp)1heTBUxI~b4;5SQnFzy@DvQM3SR-!r)6plNwIOU~fLh^TdoU&krJYr-1j2lem!tH&0Aq&E26D#0WDJD4LN*Qu&ZHpKrXE98{#(o4XE`9yF|p%8IVpVx2&!xfGstdGeWc)3A;0?Y$m*t`f=;Lp87?`supVj^+XHmVtcfAhQ9LdT19kAvBW+^>7(gx6tf?%^j1K+U*^lQ%5<~T<TI`6alzdQkV_XCaYiv2h$a8}hzAx+71gdsPYKyF|%CK3dwAQiUO@T2&1O%uO2t~Te#p`uw@bYq$8V|im-BkZe?)M|Np(NW=?P5&Gi0jxFCx8rZFVDYXCWN({hI;T(>PkWsNmw)7c#x|R-8VGM!w=hV6ig{9GaeG~#7(i65D%-?K{F`N?~JZUMALKxlKf%&#c$L#t=7e{!^IjOg7p&@C}8@K0tTbiGhsB<@?@HpG=!6Gg>s`K3>c$QR186FJUjU;Sr`(f0p2fP(0*bE^+pg@K(cG@VSuL-=xt!hf`%@4>GE?9cg|3`!KN-)u3+>WoB|rq6?E(Zdw6+(o2k|tL#^NX$sE?yFvzrsAI$}4(IEnYugHTig$lHzj-k%APA<1?63>zHS+afYWkJ-F?e*G7lN%a)8k$2hZej|^1mHt2mmElI7tMzCCC(0)XcEvu?{w$2h74~KnN4n{(5y;1K>=Kn8;gX(a$Q9VAW67`O7I%0-lCPjFt|YZjeq$(sWOZP;v*efDID*?8;1jDt9t`Hm`M0w%#T9YO4%rJI4Z%m=pyX%ijjM2b6SO|=mb0@B$P5<<^my*!fwydaM!GtR|B>+J>^O?k|Hi5N#7BfRc=|XVPFzroK=-9d^!WsJ7!1KCaqdbOsw<U-{p!=tP+C?T{#3L#(s9U&x}B>#D|LqvB6iRLA%p*7To>#fj1495il@SGq2X>H!4>K>~j)W@;9us?Ok6>iIb1#@MEcX>@Ci>)Ppd5;erF-)nBl{6h*-EJX3XdOhqXya6z$aBl4KCNtp5awJS_w$v70IfD>?MKwI#9JzrA<nQ)6;k{_}Rh2ij8p$}s^*2&cHkXT3C%jc`Q8jTn{CR0Fli<`@x!k}QMvJ=&^Cgz}v3=*orpwNXAt$tV_yKle!?WFPRqXDah5tSWWF-p1;;^sqxuSE}7c@W@<nLHJFQFv99w`22fD@=I#_-B=38NmJ6%pt*KE7V7aDEz~OIP!WT(iS-0*)gZwO;M?$JU0r%(xIU`i^xwdtX8sJfjdMuFRv3&(ypBYn>ae|5ip^Wi7*6K&n=w+oUwF|8W>eiLPeGt_GDSu#3>ZlFubcZz6hNK6@YRaJ<HiXHs7_kQ|3@aiBp5bqxelB#5G7{bSWo~aiVZw*3YA(VIZk!#`);NOGR%gRca}mP(D9QmVOg?t#iQ#CFWHi4zWyFc@C43BKQ=emzicm$R)sXBG5)9Vd^~A@1w!1U{!)&bC71l{o=&7@v)Bs_T~;&XtT6o6F^gtr>JWxGx9bS%0)KOe83+@g&=-RN>kijmM6-zqim8ZZy)wDF>46C(M_$UIW)SIN}gc`H#Utr@?VV2%LncDL$PAdxTqM(A}u&0)MLhV7X#Hn4TQdw34X9Pve8?bowt=h`WHYEnVAx^?coC@lmE#Qk_pO!CUh{HEwbLLn`$m*#qA20wKA*MdbZ5&HdGLCR-kM(s|iC3tI-2Zw!Cb9#UNfN(a|i`msmDwl&oY_TUlG2?z%pam$~_S&%Tdw66%2U?s-yn1*Sg9Tw@hgK0imF_Jd`TUg4uwML~<pRrX*GSq6_c#1-<zU(M!YZ|Ovk3rcWKVzfGEvN5Gi@AGTiQOJW}3p1CH45kx0+;vG$ayveDq0Qx=At)(61KcP|lwa8MpajC^5If9M3XxEq<9<jAxRT*=J{MX2*hOblGZw)nJCuI~*u7oJ8#v0mnx0m|p@8EccU2f?up1XN`fRrmWiybV?JnK(Si3}&kf$E!wIU%CvnRRrM9BeP7ka=z2M?Mcg?p<Uj50=X4_V%P4*CK(CLrX{Q#(C=8EV>qBIn`%$dV&ZO5-z?d4AlRgf79Zo(T#H1=|MB7$fHT#yAK{%>X(GrsNmr@Iovrz#?$+nT6S^DuBIkTy0zgL|&lKH$%z5gjk#tD$bSgXe}^ClaFYq%NOJWE^8&sXnAiyHAP?u5+dPsE}$VRjq7du%q0@+rdVJk#V(iC40gIHguk!DAGuWteDu<}0X98K@hTdHq-b|{;ZiL%?2M=60(+Nv9%2&hhqizxX*V2r+0e%~%+R|$f1BnS$Wu+zJ@k(3V<(IS;8T1Q6U-$L&7%szHMbY!KslROTovB30Y8xEX>eV-3v>{BO*#qS#We7hbQUjDR*1cLXHXuKTiw^JQneZcrXt&nnZnG>DsG=$RH!5iqeSMCS_LSGgr}5Fc`~r#e-68kEy3H0#Hm#Qm+O)w`-TPgs;J5NHT)S$!SEWa{+A4nEtkN1TIf@>QLTh}l{t|%-uSJNOF?Cs32VcZ5;kPR)<{gal8e|~@N~OV=eOpMAF(aK=1|y*phR{U%q7)DsT_uOqV(fQRxrHZM1Pw&3C&j+amj)nTa{^>3_Y#4o~H`15R^Z-6Xg7S$;;RYFWVM2I3meju5&gGEP+66;|7sOuQP4q)uBuYPYUHxP+BFkDUIeUZlPa@ha?g+iP22ihuD-8645zzB0~a*XXcf>+PgU8DlZy<(j3qynjR9(BMIQkF5UD*7@*pGJ_}5P8pz?aNfm?vm8avpeD!VGyI8y`jf8D{%Ji}iUl$4mfa}bxw?kcdVNvuG(o%|!uX%1}{NgUC>S>T<ECq5_V7JuN=0*r9#sa)P9y_u5Cvs94!%N4X{D_60!DG>krG^ZhiWrt3-R;V#=c*=YKt@I)Ko~w&c5)2!!^ZxqrpFR-9L*(-zkxsY)Js2&_05OhJuozfL6d*kPy1OSMPDbWKidv)<nUpX_Ws4FF(kLbWX9OQfFH(neE+6HLC7;KV*Z%aq-dEjGD5*|GPNH|9Hs8S@X|Ecl)L!SXLX+TqzbfWvx-_HE%(x1<z60=5v`Uv8%}*Vva;#s;}jtymRb;wQ{c^_=`g%jmsKroJP?jR*9DQ*UpigY3NtNDO;#VtQ$)&rUWlYjk-HYjPPE}WT@iKaqIIP8Y!OLC8f>Py)XJ?`dbp7Zxmeq{a|evX;ODJKM`DRP-Hb7`Z7Y9!r1^62Z!_7Me5&srfYdO=&kI_x#kuB4U4_naw9HqXm8`n@3aiL}xZSX~KCW&tBa4hm(pB$d<jGq4C2oe0S)AF>pQ*EiQW%DbtPnt@t;9m)SyQl=RW1B~L&s4uLrTceWni8p2+P-oK&zd3GJ~kI*LsuPLNInIT)N9vwXcxHW0yf)ckdJt38A`3wN~(dlxTIKj;~{oSZblGYjhBaZIXmw=!lMfDQBD&A^;_Q*$y`j*y4dPEveB;CqU$#OerJc%8XLNuf!4ESX|L}_4#umvc;>8TPhG!3|BFrL`Bn#pxTS8F!rLXhh$?*ucuu@es2VhEs!HJA6y^uMz3PPkOD?BV1|Gng4^EZUOd?>%qqGO;h^J)PlCRYd%sc`wG-IC2X7Q9Cawx~!Wb6~)93uutXWPy$(RWA83aifUBm|}6;pLGdnRQs6-=H=mOv#WGdO}zwv{64^canY5mP&1hpE^q0PX@?HyWIpvMOTNzPgE_N1Vl4A{zwMrUwpJbp>Gd1rs7>qDMnbn@X)uM=tqVG+Sx^=OqS+D9nl!ox}Fpj4j_xrMujG33Qk3=Ms!r9O3x?w8n1=_oaAxx5NFex~<K75wQ4NzDpzXg2mKTC6&os3oqd!ual$X`lzDCYSEaB)zV?D&N|pk2e!B^JTKa3G<#{S^qwyfSeWs&FUWp~BZ4rq(!H30MU1|XE`lcN(x7c&7|*H_Z3|sYpp-CKbsBJ^c6uc*t8p%)CT5yKvf^=3*rqJ;j-n}zGKj~Vl;#o^(!}b_H6yc#6_PIX%L%V!i=isIo_ueygzC9)ZBJie{(Gwuu2bQwbQxu{pwk(wDl`B|t#1n!)rVrP4-34^LmG0*<`j-~OKY2CW+yT9!kim7H<eBj%_~mFX+|zLVWx<Z*<L|vTevx?RArS3-zy3eh1&TiE3@djj>(C{>T9m&E6oL~9Py{dZvSXxm(4}VE=K`^FNEy^fqoIfd1Q`@giX5tVP!{zQSTWkXn<F+Uu+#R&crZ$z&+*feqQbi3I94m3Y__HQ94YgbjD0oQ$~TIB+rvFOE4&XP1BXUmR+GPDYGe)-%s*UOQ~#Hc2SvEjNG7ohp<vLgF5D3a7$6TJ$;*;+Eo-F;``7es@1Z$b`E`0<pLiz9~885eac&nvH{+TK&O-7VPs^O*{hzVIe|-OO9Y9c^R&wM-V2hu{xmqU1y_zrs}L2mm1Ub!Mm>oH7^mhrwuqOWuiepbOJnm*>Meyj!cr1K*^^IGY7HA0|ISrS0p`Vc;M6%JOb(f=$Vzp<%tII2g`K+5l*9}CH!HOlP-LpKuA9W4-4s}CsuH#%L7f(ztr5GPO3n-`Wku4GfcG0E9kVngm*sO_n|LjJvmm>D{)*6&F0)B-9&~#d?3jM$(#5o44DVcqh&np5g(|#KfHJIl`4bb)nIb%F)PZ(&SN1Eam*|cZ%Sy)svgmiNWdUhCKiv>zgY8<?LF{Q(=d0dIQBbURKN+VBTvB7$X%(?w$EMFIX9)~70Z4cuLsNQX6_MSc?R!;r?6s7GKZSW|2k$-M7F9R})=rA9>l7XiuMrIn{e6cBH80RS9+9-JJxvKAvO7!*dfMiQhpC3RTgsNiHJV&;+7Hh;tQ$^VvrmMJ6O`%|cTnMWkZLkPf}5md3d~M%yz?^7YXoU*-6Kzm#?<oQVyWvcI-!__%bbBKiy{?iMm=hd(}}b=;MK$xLYeF961lAF2!e(u>>`hknw7CorDiJ=JWd8BrE%SR>H?Iqke<2FmQ^$y@ON?>2jQO>bZn%7>AbKqRCG8RJ`2mIoJ3V5`m6<u9Jus$J^kmnQc!-ximFuUQ)(tSmKKVvY=2(X^MG3Qo)j8KYH@2wd(vRrT&w-gW-zz-LNhW{)Hv(%7Zz?2t!t3QFIYd(tzpS+p08$BGHwTEXX`+@x3Y)XG~F4$cnY!LRf?J7;<%T>rcxU$rorh-QwbONusv#})^K=IWZlFADc_rZvdX}Jc?7`?XhU02I_sxP{<{!z!6M|9(r30vP(c)Hh#FjX#if8h772?OS33MZ85>F$=!~+*S>dgEqXeCeoyIiH<ATdk!3S|tX-p`~_nUC9h#JJ~(#vc@;0*Tp8Y}8m#TJ7cGC`U=5de`-=D`cajbkq-^Mnq^LiAy1$?3MBwkwS2_RiL|>X4W$x=)_3x1cRWD+QQh(do*KcMeZIsStk5_!b58b1d25x-}Ba68MQsdzL|()1G{?p35HlauKPEa+h2<YI_0h(iF;)FgDifsa&+8l`ZyrDb;0L*oTFL5R-T{ou_3TSyDg9Vk-&3w(49~7)d2XMVeWhQd@T`KtDNbLf|bC*6U)ZDnXvGD}?p~o_<eqh&sLW{Z#SB&262{HnKoquG=EeBAVhk0a&!F$8(lb><^UInPZc)>}KT(S(R=|4A9P@p6()AkXdMgPFvN<(UGyV@LB32AO%{^h5S-)J%g|4WHr>b+R0i>_SDtv+0F1jnI3O3qT;N!ync_j7kUamblPbtG`4cGp0x@Xv{#Z#S^^oV-UczYa#V1sDE~V24qm^&C25JMB=At#!huU-^z@i$Aw)h&yAOcOx;j-S-!77GXy*<9lOEZPTn<cFf#i9S4|%?yJXyAj<{rHMl2P{MaeewV!8c|CSmnQ%Fv~h#535t%6VUPT0E#FTJP^v4Wi~^})9$sgWHcxF37#Z1HoDt>HP=tvITd!5Sjw6V`8w4(u5|T&qw;Td9~rer8VNm~8%Sf4ZncXUe0a1H0ILctD=E6&&0r&<77+^Y#lW4)(G$pQ-Ao?IpOJ#wMU9$xD3yS8ONMIqR#(o==1T}nJXX>UxVW&cO@GzZl)FGcubE;Bjvj`TWcdLl|F+C|i4c4zOSP#HJUwZWWxaWct69EhR+xthXIw5TjHVvZKNj!^t9sZ9OhT<bnvqdp^*JT1XOQC9>N6`*hzM8ipRcQ?El5?!#by8p$)hZ1l7ZGT(21sANvNIT!<Hbihp)T!C(R8kWztPN!$F8hMM_$k(d-H`V17F#+ytz{VRO^1&6NOfpw>BC?|cOA4~jzhv)^yN*jh!Qd9<9!N;?eFc4BVWEO8+p$7rQ5B?MHDwBy5H6?%{C2a#u}LwKfIDR&D?9$k{)P85WAgr+{8rWGTWda3Ry0LQe>tpxkz=u?#*UE~EGUh%H-asc*~f|8Yfu!2l}(vMAXek?vp+z=dF$zzegKjlzUHLrfBqw@-2!ero`S)<hQVr+#5AR*%O+k^{YmVtFpY_9Vz<g4~p?PVPsAXv4X2!NeEu8mRAqiQnXQh%K;nSGzZq38yFt>a{=8zt{u77ev!nRje$)j26^UZD(zTqi-C5_^uM*eaGD6Ih@M-2H^$o#W`j6&cN9K$$4yTl<;SIabRENeXNd0fRaZnWW>x6CiS77-6PBpQ_%6wDO}Az@e)kw<ddVzaQgc@DWXfbW1o?X<w~$C4Z?U*fHY)o$aJSDSCnk?w1GHRNw%3@u9VGd3~P(eq&WX5=Ue|KWRpy64I9JB^z}>ripdFv_SHRgRr7VbkIYJYNy6wLt5KUS7``tuOddQ^7;%n249rW$%V1gk|7i`e7Qm?vx<^yf`eTbu5b!dhsMoODHM{HZ12~-i<BX{Z5hAV;GxVCD*-M#hYdtM7%!SQEpSeEakbi@%1^U%mb$dLUcGT@ODj1OOV!oxk2!0ho!r~3peM|iC)WBD;jFR*Ir=L<B67fo7Gz=Cg8MaDuh~sQDtDIz$h^!CEPusaY6F<6QGIHA*-RMWYXvxYO<qr7g90%)S(4kvY%Ma+v0Bhq6*apu0V5}a5!{Vo7oXsk+XAyh<ONbD6}-kpsYcl{LgY*b4xb^6QRS)AJZ!wD1u+F_4a$QAozvN(rWLi494S)x#Y|EZVpw^2ferHQd>!XUEcvyTnB(gNr!fW7cwdL(5bBMr>bufAmz0%i3Dj+0PM}g)yd#2ar&Pej)Rob(W2yT!wYf<Gj23Wl(}_xf%zAEDBovjR&Q#Vzjk%+d=;uzO+lCi;pgO(Iz1*d^r~oYBr789lw=cb9<$`?}KbVI0-l`xZ7k5e1s(D^VR*sw3;)WC#*LpYkm=UWrAVX7eGIjQ8da_P2UE)fcXn{v@Ddc3*A}I7|#Gc9c;EL~AsHtYwV5BU@EI)8XT8SYgq+mIdmXq>C)`j~?sqkF)U6grba-{V}LqLn8giLG6%cYJeg`>()81AYllPUY^YP`CIGL?3;QaPuzZp$rAgn;iE3Q9wNPpU40BdlaWl?=YvUhw)%{efsLoQNDI?$Z^8qN`5OU}I~Cf+|A_6}2|DrMOU%*c3&EVHv!`AHi^IAmxnjgEF*gFg_iW%~zKfBxY2xnrYf#(@f{gRB{fYDZO6_resfCfvTWOw@~5;8+RQ}k2jS33XvEVNu`%ZnN?WD&jD}}g6xR&{LCfA;&e1O5aZrn54`L^M!L>Ro@-SM?I4va&bs?uCl={gj3A%*0U|Mlmgm+eE!(LmA<6@UepZX?>EthT)VV&eo>NJ7k{Y43YDlh{&|hah0wq1%=({>8X;1qSriPjhSIu-j8_|Qxq$~0^jh?QXb`fO(eh0-~j@ET2Z^<rKO(_LtMQ+F8cxF^TDX>AUHV#p}n*2tUWnkK5<hxlJC$t_+{BUeINZfFM>t{05Efyn2IzV=#>+qN<yJ!B4mn{=Pda;Z(=>a5V=My13H&q>b>*mOSUisuDm;)m}u+@KE%+lmu{>^77I|NJ%5neYk7Yv$+TE2VhlJIE-R`1qiZA%MJx)hDP2|wf0H}|lSpamu-B)(U~WW*J>pTJ1~hfQ~I-1;7!xHp(%S}WB;0@_7={RC6nJu8aAf@v$kIpX}I9jJsy<$j>$>)BGTc?_O^#k~aQz-=}`l#Q|5A-5J$q(l=SL>)|Vkgf~N?9mdLE?U_|>0-xhqw<XVJfcJ=!1Ggbiupr_5$#e04_R_~8Fsq`ainLZ00uD2iCa}2KySkP3qi#*%(Q)z*+(mNfXXe(h1}B<9JC#u5hAKh3Fx!*2UuO|=o|?Vg)jp59}3P?XY5IJ*_=&r#`-jTzx(SPZQE^ssEHd&j>S^DKMmrOufAF?l>5F6Uq0|%hA;1z*>5M)hyMejK`3<')))
_PLAN_IMPL=make_agent({0:_SCHEDULE},**{'hand_align': True, 'weed_repair': True, 'sell_lead': False, 'budget_guard': False, 'room_guard': False, 'clamp_sells': False, 'dead_stock': False, 'terminal_liquidation': True, 'front_run': False})
def standalone_plan_agent(observation,configuration=None):
    return _PLAN_IMPL(observation,configuration)
standalone_plan_agent.telemetry=_PLAN_IMPL.chassis.diagnostics
agent=standalone_plan_agent
kaggle_submission_agent=standalone_plan_agent
