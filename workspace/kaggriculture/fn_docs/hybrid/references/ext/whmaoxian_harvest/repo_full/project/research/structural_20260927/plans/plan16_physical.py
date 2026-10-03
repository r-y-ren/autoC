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
_SCHEDULE=json.loads(zlib.decompress(base64.b85decode('c-rk<U5{MXar`g)ybs!$-4&U)H8qw9Q(A$fJa7a;Fc1d;0_VZWTaf=AdOv3F+^(*w?sI0z1b)(Jc6jgkKHb&T)xZAt#lQafZ-4#E-!A^?*NdO;K76?Nbb0Y_fBuhu`OnW^eE#^?KmYCD|MFj-KmU61yI=nF+ucuZf4qBlae49Pet&U!_385Q>!07>fA`CqkDtHa|FFCJ{NI~TpZ@3a<k4^6{Nb0M7ymGM$%oy$cgM#(yx@no?{^pC18Ljg>kmKdcAs0YT{rD_zr20--EW`!{_&TGryW|hX!X;-eRwGU^7!)jJKojxh`qaevwM2rNu&0=4<8>oefaRx{ritUEWVOM3g_%9owKJOY)_i8e(6a&R%03$l79Q|cf0RSJHDQ%<qMCWp2zKR)Mt&wQy-UW<Mch3sC`cx>eq`mcX${+{JoQx7eDUa-T!oPx$)Z*N9XYsm#AT@6|-!H?B<92U)Iwc`-zqv>YnVxddXekxqaLdhrf^xJ&j5-PCtD-v~KmHhlwi<)M7u}ecZk0uP6`I`bmoyKaC=8fqLK5IEVK=KLMRPu~*?wkB{{>-)T$Y&9S<a+>w6zo9g+Mejn*?d7zEgg=g9W+<RT}X!y<iK@HD7{lpIz|Fk|n@_3+~oGW9ay6VhJ4=>xTXjtR%X1(Tl=-~B0K9O_u43B(s|L)!H&Bxz<zkC1j?Yp=Cd^$3xopx+X`C;|`@7~}4oXiC?)K*V<{wX~74tE%__ZHn>+0oF#2sZ#9#?Xe6nE_@UbgnR3am-`$4&R`jk!P=MlFjLR&@iQ6@9v%&^Z3D=IB&kdf;sM*!+V#<(Ss><`Zi^k+-egJy!2oO$D#B`Kp04%`?!mj><`Zkbq!j3c7UmS7?kkg@yBv#Hh5^ZLu&@CcGSeC#SdP1FkiiK7_*hhplg#qUb3afp|(4IW_WbLO>u^T*!4qWvTmmHJa91_|8dehYaF8enJj6`t1LZkq;b)~p~hliG#7sT+BE)p&9x>vi19)VvJ@;i{FSs@B0K?hO|)Pvz|XTIB<gpiP`{x8i09qWOuHi}U-)D|jK-y$m~C+eptCABq_U}x`$jb+9ewilCwokHH(HBkcdaWfvA%@ex`G7M5-8d5s6`uUDE@Hw{*NgJl#PvH!hQJo{%-%f-TU`{0t1JvwcG$fbLSlvrAAqX?bF@0cu+E@YE99mFiaNRsPQWW;uT*Hmg?c9%M}DxQ|%63*&4>!udTFRm*eE8Mjte0@Pg>IC0bF-VPzZT(5%Bh7&QIjhodVDdOoYaPD9qc{vz+zM&aNK;6$FOd)eNb-n-+i*m0vQGrefKvjFiq4EN4~do<lFi;6WnLZl?Ph`eiTOH`uwrK_37D2esn@Gks;Nu~kZ8wL26-9v|?SH8JoP};V1I_<}HMV~^ypW&|SZF!y8^wj7wpjf*2>;XFBf7wU@OV+umDIo6o@A|eL9VQdD-kglokXzQZ<_k6~v?)g&4F?&mx*oF({dNOh+EzKd^{X*R*B<^CdH0YLG~b$=@^0pQPBB#xf;{&P03ewA0%^ooVk{>+oDUcv)zJf^7J-590sNQn*Mg~kZJPR<bD8?U_n2h%OIsG8!9zxV!EARwoxyNl5Hw~Q(#&)}ygM=pW}@zy<-XXF7G0p}IIM31adZ3D`f#+P79$<;4ZOQ#?}MZ|$dH5n&Matfq{R5JV*7BKx1TD+F{^L##;d`;QzGJoCDQ4^AinsI=l|pRL*V;)q746+5#otFj?EZQJcq}j0M8n!qY~-VCa7mIR;VhgX}%#HA0e@HEt<pavG(|j#;VWX&>lg{lx?7@MH|i;cV@o<(r>4u1NIvYK~LfMc|mU1P~TQ~9%NnvxINuCEluFy4HgOVQ(ka(8?kT)_Ymzu4?2wHf0%J!%8ZLAr{2euFP*=kg8X?TVhVD~y&O)wGtquc1M+%(A|HcWkaUHTmf@F#zFFWQIC*(qe4p_F8aY=W26zeclaHTHsBey8vcJE72l9}(RzVDYOY=NN$~XX8I_FnuV0kl8!1`(2V;kvsJ+1Y3cRzi1q3!6yI}E=fkJ|%cta_f)heYTDAdjy!z72#sjyBfw-(sKBzkubkxUum+>#dz2_~6eBb%Wf@z{50re}DgBhZI*HhIG>r_Q)W4qO!91O45zvgdF-%H`l?MTFF!Z?+6gv!K9#lT^RaAV&STq>I=pg9Za!vX)nvE=h5X{G8phGkIM=uw1l*(&NP%pJ9Y&CDa(mnFQ@hYyS(bd0KB=s|G7bAN`yN&K|%WQaZboOV)-D?uX-H1@^p1+TF<lKwA$PcJ?tyKC0P#k-)XkGJ9Hp^&W=1L?viiPS#ik2bC(;1WKrO+Q6KCUcXnCq2vi$cZjbCjR6PodM`@<eh9l1<4q5KE8jE<IWX;0cO|@KBtpI?qZ27tPV5ts_)qIjf)}f5mIZ9ul@Qa^QD{ny%6)_#p1TuKp4qAE4vLAv0UX-~xN5_rOqKx+`Pd|bcsfj(1_kI1TpPSsFz2(8et-2na%T8nt7!8y_P>y5GoCYKCg%nzp!%U)N1dA-3H>F;0oA4d=`8L+>0`uuZo=m<bZrc-k!J~zmKrl?A(4)-7FcS<3?N*R$6q*DES|No~y&#x->*HjrO%fCPeBFs{Nd*awH;DS8ao=XBD>H_DVOe01P>$@j?+bO-ay%u{K@}J-Rp2a3JG9n=QsyY!!2on%&{jcOGLE==%OkQ?_Y8>kz~SkK1#mp;nfya*fLQP?YT2YgUW%#KysZN2Z*V-6i#?x0L$Y$lakD8Qe|Wv<;cyd$Z1E1JYEn4!EuIJ?=2L*Cr7C7Z2J^rJ5aNFs5<+7C|M>RZA0A?!93+6wfC(7H0~z-C&=QFXNVERh<d0rw$CY&SQ24cB)vIyC1O|BLv8J5?{6E}uKF%P(cdFT{Jq*DD2Hp}dSlpDe0q$;ez|z%rU`GH*z-&C-X%!)Z=zm6|gIhQSB1Umh9>yt}KMG<<7(#U^vjR{ln<C}%nCn%>iUx!BbV-_fze4z>n%<?eoUYb&M5Sn%FKt@&dZ=?z9wyT)#SjD>OmON1ixHJoSa#!V%aYZz@I?4X#RMMIGZaSrRx=z4C=}&uVW2h$BfVHdiA>>|*dTDOiL2qL3&V-+p#Iiapb;=ik4%^<agM}{4(r@2*<K(QCkC#AXG>$&x*4qY3SG6koZ3@y<X8zSMqFq8KWjx3bJJAjz~j@0gK}o*bWOJEG3o)&bLm?_zmdeV;_s_IzMkymCXZfD>Yu_NS)Jb2Nc!o+uR2)*pg*K~#UqjXnv&7ERP&Mi?qIywa08Z<?V_!EAZ~>LfpJC%0iiV!$RlLPWfe=u?MT_q!CC|dsh@3OXKJ*wSc#_4>6onfsWhPlWM^o<5>$u8>#aR&Ho0R>Yds7<3ZbC!0ys`#o6$~c9#S;J;`B+8eS%g*`zh`~vwF|f=$!f~(#J}mspakLO<<w5HmB3KxU$qf&C3VM*nvwLnZ=m@c>m+w$NPSPy;Q=LrZ_ykRm2=;6a{qBEYPxA1Fwq;wkB@5Dfw{btgM?ObgLjLu*=Coq%`F;e8b7P%E`Whj87NX`r0V3uiW79jy0(HOW~T;`9EzP(c;RW9d2+_L<47U2UrSwHT>YLigY_`C84f2bI4egR$XVyto~!C*>?-OS_g-^`+x@lP=)UK55~|amgBAnL`3f9c=T2T8g6$hm!Pa-SzrD>uq-P&5H3Mtc|F~posj>E^Cz}iGuHod@5T8kf%j#z6F8O<krT?#(}g176SBiPI&)6oo8cqms^PF!L*l`8NNog2>3D%#$c^1Lwa)Tz0yu%C8;PMfDF4xl!w)b&B2K~5j9E0De&v&$uZ@im=^lsH!$Cd#e)(4)p%YQVe#J$_SAs!n^HO8d1OsIwVeA4AYlM;x{XGDM$6o{N@Gu&ypDw<~RHCQiiyMhDMSA*8A#a2+ppKX{l7|F2B+I5@+K&gx9QlZ8=i6i&-~&h?33f0>GQc&&eV)^~zBRD`n0>NbWhzDyTTTLO;^<s2d9j!~_Ior7c#cgm+{FqJ5SHH+4T5pMZ<ikZ;6CQg%IVD8bvO%aOF*vzKqk?bB7)Tf4G=dz^-__GC`I-IniXPs$3FpGF7HSzo)L`1L9r4iP+~`2B1j>Xcz6uuHpRH?2oqQjv|KWYnXtnoy9$RP4-2lb06lU#vaK1PUC1(?h3T+0O!0d_+ligcp}@HSAjR_*A?df@8{2gqaoIJrLLF!rAbOU*3t{W&H05<~ilAE!(UZ_DaOy`y^{*?C+|}mnnB0{mpM@+%|I4byX&Pi_5JJfa0tqmqatuV$6u~HaN#C*gdF((Pr&$nme(k2(*YJW}S;hcO1M?WU9|a_br9w$^2D-JtltrqMkI>MF5&{Q}(eC}ESBYb(L$O+<F{6uz^D;zA+TN!K#q}immQ1oE*?i026(}(gD@D8~Dps1rpF5&UzK$|f*z{?Mz;j)HHMqH0@YExZB)vIi<JtL$HK&noJ$#t%Sz6Wd6o{A;pXpYAgmY-AUD`k*O~$jbp)lJcES3~1Zs7n3c!*6~$!GHT)FKW!6^x>me6}K)OeT(2F+kXM``X+a&aBv>w95>b0lzi^4n0(m6kA6vV=OI9><6=3Zujyj!W~3LS6C`1`Ck_9Fb}lMV+wYWT)C0c6Jf@RDFTpulAI1rTQ2NfI4=_i$kjPHZ?RC`gr#Y_K=&AFj;@mv_k2?TGE@0;mi}mj?tSi5t7J==_~|yVQW>laE&=ami8sAImr#x_34UFpcR{8>Ln&ty{k%;JTY6n#PXu06Ai`Bq5oCi7fOcfWwsFL+IvfNZ;AQNQLP_(l1hZ1%G?r2q2TbBt#O2--+RJiJB|<JBm+16E&!0{%OF7X@bV9hEg|C~XWWiPH**n=hF#O74J&|)V5lvwb27p#GP^rUl$@7HkOv>!wZPv(8Cq}L#seqGH1M*}m2<nBO6K#VB>b#9CIkqurs)pL<3@18p%g=`sRgl0%q}0qnp=vK@NC~oK-{83~)`DfxVyCI!K|kQ<Ze7!Xss_HfO6!b+)60Tho-FVV5HOlWFh0XZq)>^QG06BbY#P&lcTT{NI*mM`iS=awN!iRfQ6c)0R5+yTHzQpGn_5*LDjY>K&}$R*DtBpu9+o0>^YhVS)@gzguH%*hu{0kQ*Lg_Kfh@RDFZYYJlko9cbrfj#RMNrj`|qEurgfORm)445P)DDutzrpM6$;#{D+FYGG5qUh46?Zy1;PNVb5rP`=iIM93}aj>hoddU<v8}l(ffaaT1lQ8rSK~#Y%+?)(g7EqDm>OHEO4Uj)N&1d1s;XES@75yI9TZ7=kZbKHuR)2X+Sz5t+3TlwTqjmRy}(XtP^eAN+uCkE*oPCAvD>?5?tAr$r;3j7J~l47;m;iE2Vq#(+=BH31*)7IDi0`tD#I->oYW3m|ZOSQYXhYi1J;1GbsN>QtkzM!fvk@2Lr`s$qu0MiBG3`IP=D&p!o2s@L`ZeF^htNuUJ$t4ek3nyM_=VmKe?nBl@_jM!^wwJRoI<RAI_5z1pHuip@;{5x*oscl|?@!DD}B=#*SuL~UaY#mvRi{OD=t@01`EZj)-kbiBDOf+d?ysJLb65j?;^*9HtEfGoNlr_5c&Evps?%Lq~5zD(t?Z3@2nh!AK04FN${m5$LWVxeFfLWS@ik@bA&kP(%3RYy$#yuN5ufQy8YA)~H)Vy%=seu?zdzFs6~!AK*~{vvwJiz!*$AfG$){(fQ_7BJ4e;!MEQU6s@tEF%{A7KH%)o=0{oII3P?aZA9YP04e@Z6%g2Wg?yK<AFS>(q3?wFgg#8SYKsw(|C=t{fK=9use#8OUGmz9FtODo#-h7INwMp?g|%B*($xk8A&tE3$MYh7W}Ne=<FA^)=cLF@{;sQ)R5<Ip01!$^rP=}_iKMp>6`MWbRSo-spAbk3A56Id^`h#Q;L{M#h`|GlQJUMqqRLQd5Jp{2SH=!6_8)9|BZ3D$D@?wi)ye5ZEO3Un}#=WZkK<_QhrQ}$LHVz%J65B#j2MX>3=@{N*P5tSKIo{6qv))98YOY&XwrMl;^+_aG-CS*>!HgJ^pXm1>CC3_vpX9enBn~+;Bdf$jqD*Y4Ik0wykJWImA)0SU^VE6Uy|sYi`SKZz2y|^ZN!8?H27uBDrv!Whp^GTM~#`s>3Wvp=RdBv0R!}bvc3&=-l%G5UR1V{CjCVSQx}Z&tFv%p%jmdfyP@y1UKOgpxLd^rG~O>Ksh@nJd#j>3eI#p$;!?lvr#1kmbpS=JpNeWU=b;k0!xtTk0XR{wH9;5ovO=OO)>%Lh!(?vr7_|}Mb2g^dPY+FKH-`1ngsD8fmI}hri(8GtL`hFRFyNOe7U~NY&I;Tt;aH|E=W5VMwch!i>CpOxqB@?S3pzb-ODVN%q6vE^K|2Bu#qNM59E2U=gEe5TzAC+feq5?IN7vhqA)V==2aUNEvMLI3`-vWNo8*GcfCkTr2<p&tSR9D0pW0B8<YQ~8<C-Cj6IXi4Z;oFyxKa$&PDclcva}CVa!cyKW3N41Uk8Hu~92RTx^xJvdWh5lxKOA0sMo5(v=P}(DVp5*ADQHsmbc;X=U8948_<OmXD8o=cOlA?UjnYyUjFva{0qxe4P|C(`7W7We6sW=uhOIh10P-1_d_SmSBiCWnNkrV@Qc=*DaZsEgjzg)mCW~3bl~hZN`c+a*JKl{mR7};}t7m4wc>IR}GjeIaa|G2DD<L!mdcAAW1zr6Q-4=P_PnhxRo*kvNThLkCA9vS)T}sM@esuTL}jAT!^nRSFDgMO>qLMjk?CKibRQB&Std?(L6X@k=CxJCxf-_O8ofA6M_;^%Pfd^V@B(-C7T_1W`bkWJkf31YX(p<3G0|CGBY^}T;l3@!F90&R_APm%Ndzdv{o18?7P{ZP;{txz*jMS*rKMc)P#LP6{&445Q5BP3>Y~?)VBU+Qb8C7U<m4+`^n=>dD)$9F*9}<GW0~{Q4VBDYj%krcTKWhn35TsU2vayW^b>9VB{e@iwl@k!SkA${IZMJDQI+g{<)>qHfUWf`%np~rHPb&!dj$v5zb%GoJCmF$J9X-Q~21so5eRzXklMj&*A$?Occ}@kPzq9r%_%06Zh__D8=;!g!!+l%r|CyGvF|Qge7)mL!^wdRfdJhNE+($%N4bc7$F-M(W)txixgD@|18jgURv%<gfy*+HMS<U!4WATR89pZ-)MAGuO_BzG!@fG0qYz{F)IxYs-pq2Nmo%=B4D*bHm-*P;4QTx5|SlX232aIg#^mDjC?*<OwcA7=@P9!!yeJ9OzT#v&I{`uTmh~UTggxH;1{szN!TBHE18{(U7Jz48aqsq8LXBaQcH&#sl{jkVho`*X@?Z>E4dRG^h?Dd7%tAS7r}hW)}1N1UVzG6Ew-^lLJ3C9#J}9^ST70Fpc%F|yiAU#a!9U-s+B@J6%99aw{QnIrf+f72CE}7)fBEVO6v&Luq|q|K<tJ_|7d&EA%rrw@-gl$1}WoGx|GKy*%I7LCPM^sfY)-N;)G18n$cUAZ06HETD{VhbST&fN3e^KDQ(fqLcU%N1Z!oKjw4~+Ogp!nRS5&zBs9uuH|@)K5zfd<PV;19a1JF9R}cKUGB|7ON>Dy7B#q3a`!zU0?d+hv4cTeb&n!CJ$t-lpm80Ne9oZYgV~TQB1lwR_IbFZgS88!s38T_zj4y>+_ubp?$Eul+`y~(;hxW~pM$AN4Txv_pY0p>>f))gWe!z{dg|kcC+?u{L75ic#XmAfxsRKW|)yr3k8%Q6#I-iadOckfXz+RErP+m|PT)i}J$srLWb?f|MXof(StqvhfbF?+14poP>Q}G|DYooBGRD@k6+xBI>_IZf~S1YLH&eNr0meOS8FOfYgO~ZIF(%iJ?`;`*`^Jp8t5WGqq+jbtW&Rhg{-7x?Je*Zik%qO;UJHP4El)UtBy!EJ5yqB5Lp&x8U*tfifaHFb%pk+DtAJM0HUM3EqiW8s<$@JF6_q3z*!O9S?6LavXtA}kvZ;Dm~<k0$OV(GVl{IiL)vEvudK_8bnhf@5XaWMdu$(vtYn#>?Rw*B(OC}v^benmX9?F63L`sh&B(?l{^qytUlk~NB4!a2V+ihnrlu_Wh=W^8`lbusD9s<!!y)W3`iOi;>MjwO+EI|IiH5NOU)`tm##F}dJ?y7Hri-%3IB@oPXU@ycL=N9fuLwy|3$aj7l?gI+x{Ikzgip)ZrX-W72B!qCV@=TmoL5+$6jP#jSnv1*#!EGcwUkD^<=dZsD%h5ZCb8<|Rc$joqjNHG?Q7Z~sGAfIFQ-C_rOvbCf?;vz#i&$nCh!12x4^{Ci48cwe2G;;9-JiZZEikQp-<fJ%cpM_?K-Fcalu8@0jqpo{A?S^?AX6V@ZP>DEPC&sHx-73mzGSZWM?XsSrps}nfu~^B>%)Tm*KUprwO~bcWS#e?Yp>auEfAXQZJekieX<CT=FkaWQq4YWuy9f}o0)-s5=Ap;73!?mUF#_izfZYN!^98wIlH{c!+D4+|W~}yRbf-=g&aR2V*>?HW;^)4c{y^@dP4Zf9k(f<9L1rE1$p}4tTa4MwiIkAtw$18OsFcafcD&0KHdPe>;wq&?n^Ik|bP2e{U<U>Alvo^qa7?PQ!8@pm2wu0*oLp;*oS>eUX|fHwED#l6wy>oAu2?sPK?4YOn~;3t5+sy8!OLv)k!5+tdy*z*QF17x1SMr_kTRESri#3vz_q*Sg*?Vgg)_u}ij=`2QMn0>NVSO7O%{=iH~?;_ce(Iy^wk2EIVTfzj#sdW)1Ob1GpCFfMRZY_W(++WEmv9-tJZnC1x!|1<*NYG3?Zxnu2Nwtd5V#3X0Tv<*aV~Joe$XPG^w$EXvI}z)Ndp>qX*<0M%Ro*1P+*j`lx?*&#ed=4-sZz&=`@h`Y3o*EB`4uV-|?PEmDB@(;nP1_$yPx;gM5ck@k7Rs-OuiQalQAEd;I30b~JCeS}h#qaUnv)J&F@t%Sm~G{j{zR@k$hy!ee<1p_fZL`^ii*e53*<g$k)Uq|N7+2)L$&L>%A1*xIBurn|w-26cygXMY@w-ZH%xTce#z6BSV_F1Qpp)$So;9a-$bGw-=QIQ`6!bJp-8XUU(Ln{@E4wtA^s)-nU3TLc&Fcn<U)jn`^^6e4xJvAq1M9xRmcZI)@r{ztd0SeDKvL!*df;&S_Hr{S38W8sm7L|wG!-A9%N#mZeVMJ{PKN<ws8<b32OHTzWh${M+dS<eEC@1p_W}9|Oozakkk+$rKr$H~7GIbI*A}=@Rab2uH!sb&oy|g03B<?^}o`ZY+-}Ew+CI53@4!%*QOCMe_6OUy-cr}4;5W&ae>ax2$)0eN0WL-nh&9ABnPLczqUQve)VXG6TH)QUmKo<>uP!;!@#CtJi`Jn?F1HuBh3WtfFN8;62rFK<8M5x*oT`9-FZ=3cMMXZ1wWpvp8SENh^+Yh&W`St~_i%`2U9s8#4(%BO9fOP<j<$aZq*T}&GPEkn>-%G&iWIxR?_nDMVT}n$Cuv`#h2$*C1M5c2AU>KA5(_-g{qBIQMR*4CekV65?f$jS|w4M+&^|<mv&gbC~K~HxYzfOwf=(Bf14$OXM2-Ywl$RO}IB9XH^2LXXDw*!j)@ra;TGi@B+qG(Ev(=ARYSH8nySj56iT&1m_q8HC$TQNlWEX~r;y~&g*V(b8BB3T9?G2_OeE^1A)+2oMU+W#E8cUO&Dps1!dcRdIEmYQcweNwKeiL0nw?=)lTc{<i@-Evkx31YmKsurp>YJ^DKEW-%-`Meh;`bss>TG34&9rIK-mCT@9SMdR(c@;65TaaLPoobHPq9Q(%{xJ3~IjL9@G-~Uuy1aD(h%$s_aDC1zD78(o5t-cgb*V^!L_HJ$otTlgnZ#UjWTW5=L2M=3i-WZXUra~}OxJT~tbmK*bPhpTB*TuikCT^9pE;p84cRMAwIIJ@&B~cP$YRS>x?c6LXbUlO#48H5a4HF4%r^eb^m2l^uLJ14emtB2yyvf2m2@@V@P3qGMIkbiRSjrtSimZ=o!!tf;Dm%Dskhfmx=v@w(o{EE%QOvC&)|ZIFf<1rOE~5lVs3IEow&WKYBiKvUsN}QJ3(sqf-t&s)#S^E?tWh*h2)Zl6ej`n>Y89p#-mw@jQgFee2AN<H^dRV{nSwS^isR{c((}-b8e2J;529HS%A2&D(EOs-ynv^CDv>n48rL6imgAJb4cf-uX_?~ccQIetIfeF>A_)`oF&CWiPp~GEy~KH;KHE3Kqvu7QySe|#SBWj$u`bf^{7YO2h=Y5M?bx>o(rfEvZub@hT!z=ml3*B{H|Ds5gkl<PW21r1OgSSJyOmwrLKmB+8I+zC|~t8pc{(j7+mjSY+7Qm#<eYE=M)n<f&D<lgd0GcCC?)3O0Y6C)A(XGFO0`HyaaNZqES$94)_^gHOvtxFiM71rTGwoW$CF7*o9V_y2=>~Kn9ylo`3YD8?^&V%tnqjXzNaclm*_vmFre9_M__&a1R(QJsEeMs!68m;gOh^XS%2Hd)28;rT!*sCyn4)w3eb~VcTif8Bv_ErH@n){x|l1B|X*w+6n+l){(+~-@*i#%VF7n3X52~q^w?Lp9d~JHb9*8&yZvasf3o#j9ih9yL2DQNWeuyELf~4zg1nJwziw9BnjB;8ErI;lyYBW3R{nvmQh8DPEmZ6qp&m-&9ksoV4;hMrxX!A4Ux1^GD+{J)OTOxof;u|&6h{$NvHbhY{_a$?P_DiyhxfSLaEh8rzX(I07!NM%zr_0St_wf6|++DP+J8(Tsz}rvm+7l`9qUiQ&8UkxL7WqRbZC&xIh91EA(r;+>|1u`;3v6eoYJVYf{f3f&gPNUa=Q0U_S#%7}Cv>(ju*lFi$iK0F#JjX-Z{Brj98^Q%vpJ6D1|QjJz@d%?k8Xzci_ZTBz{cjm~dd#R<^#lYCwoI<1(vlL|;;!PbV@9+EN=SBenUm=Ud3nj4-Ft|FAQMfVEv(;X`(R=R!0N)7tTaDG~irKxUZ($#qaM@r*>=SQWaxF45m!*M&KygLYoP19xwepRavOKN-0s5?TJVM$Lx%V?D|8|To$047BB7xpd|8$M*WFgrF*5~I2z=PLVGuyNTOGfqWiEirdA>%hS`6h+1z&C!BzB1@4Lku0xv?V(>SlJFuo!bzlK>TQ%!$8tNw&M#IUMetK9;eHJnU4=k}j-GO%vTU`k>0WfZ&jYH`c+MA<@p`_)4+1T2%{q(2Wn2txh)U>O`A~=#gyk6-VS{uF4q912G{MWA$zYlk;S8a7Dc-J3k}L||jUjGYk~gJ7fkw*zpu4hd+g47V2TAQ@#1G%#^ffFq<c%<crx?;yi%L{YOMotuNYd;Klc7^shbyB)(Xz9+Z53*WE^L;4u4@5pCx-HwGPNsOLoSPmxUr<X>0p9YC#+AKllM%fpFTHFOO_F1x=v*B1becQvNWn>ytha-OlzoA2&f9qS;2edJWw(NxDpyWsm2x&syG@)aKs2n<(ST9E-<K6wHS1biXsN{az)i*IbZ@(5tI|iO3VN8YMBbH<>h0!k=L;MyueQ3engf_OebV9;C(JHD`mtAnRfebz95DAIxXyh#ll@<@?53$eS(Kn1zJIGJ=~a4V(Ako;lg3#y<+tabC=bny&7ae>v%pOWqekB@r*K)>udlS<~b@d*FG@0P9fdw%E|~}S1(=;@ie`0V{kmUmZr?PGbpy(0wY0swU#P(xz<Iwth-$arvQ~$zN|eB6^?;I^T4uUXc*;NXgQx=p>*IYkX27@4Lu9ImQOqFDFgANQfE@>z>{c`iv^yZqPT*W^(1m^iu;h71_d4+zdr3HQUaJjqSgYQn3cQL6y=o*EpuOm0igvS<kCayY$u8myJ)DC?46hn;}5$iZ;gWUVAiH7p?ev%=#z8P(MY6;$GqagJ)_WW4EBlI9h88>SPl}0H{&Ul%Q9in<Vjn+WM@SYtlJy5BEjA1(Lq_Ib3;68D|DuNiwlOr1wRT!gwS_Z1Uy!WXtL$gxCK1V-KZ870A0<{w?+XsinJ&rpR>L2vA7EG)O`?I{|mn}<^WL$Xs?liZ+ps4mV}i6&ppv1pm}(j|J2IK+PM1IOf!JVy#VFWgl&x+uU!2Fk-U&ne6~%5F8*;g1K@;(y6`#$fA(z~-C_-1odc)}dQ=r9+I+EVGW||&m|}L~F^uXE!5Wg7)$;M|@+i{1P%pdM(S-y`?q)Xv#?HR&WFczQnMuYqQwS@3Yr#jemc#Nu`PNY$f)}(=mDggk7^%9=3hFdWRZ@NuKw2%@z>Wx2{aR!MR0xgTvDCz6YS8XW#oUUity~_`)ZEAa#GooTLkmwT=0uB#rc1|YritcSm=5$IGscRsVVbGYakD&alDbOHctDh|RXyvT)=H^F0)COwb~bQJvI=6d37=Y4mQbTUG9xKA$KeKgM6`U&2!QczB|C=<ju85%tS7q0UPDhzH<~RQKnX%{5->VZ6&z+Uzpen_3PwTN;;eL?6^K~1@9BZdBBgOQq4&zFFS4=;om?}+=mf|Aq1i`jTXdv>v)+k(p0Zx9K)~lU2&14>vVpw1L-#;Gg?Ji^W)j(>hu${$tTtaJ&``c;QdujWn)|Xvj*L}h;sH|$qn7?b#Ln!9x5b7r7d9_9!}55!@dg(@X*g|UBSXbb;+;UfK;?&8nQKDvzB;BeDi0aj8TA4_+(D}O9o$^1g@sWJqevEM6nC>GSSk2QN0Ql|6d$6XAT_2M?DX3S%d|!}DR5Unx4Q92zG{Vl8G}V?E5NdY`KrvtU25)n67*p{rn*BJKWDAV;J5n5BU5SL<mg|J=80<{b?UiivK4ZmDF_i=7`QrO^O+?<T$zpo;~PKGu84EOdJtpU>91>Pp`s(3R%%XdF7hf6ojG|OPWtO{cE?eLfb5oH9|`P$Dz?FJWIPm#z9qqeypH7%dTT@3CAs7A08V3$Yk?fsX9wHr3t|*J;sow|u+0Q$1U%7@vD-;69$JjVUbdZ$L`AW<8_h{Y5%poFUr16y(9F}C`@0tPr~d_3s5LA')))
_PLAN_IMPL=make_agent({0:_SCHEDULE},**{'hand_align': True, 'weed_repair': True, 'sell_lead': False, 'budget_guard': False, 'room_guard': False, 'clamp_sells': False, 'dead_stock': False, 'terminal_liquidation': True, 'front_run': False})
def standalone_plan_agent(observation,configuration=None):
    return _PLAN_IMPL(observation,configuration)
standalone_plan_agent.telemetry=_PLAN_IMPL.chassis.diagnostics
agent=standalone_plan_agent
kaggle_submission_agent=standalone_plan_agent
