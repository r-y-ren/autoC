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
_SCHEDULE=json.loads(zlib.decompress(base64.b85decode('c-qxn!ERhflKdB)c`&=%mb^Dv>am59O+liDm^B2$z|LZU#q7bmx5fVZ(jvS2^~=bJ$gFBwKA9#d_Ip)XS(%ZMkw5?Mvw#2fw}1ZQw`c$I^Rss^KYV!h>FU{k{Q6)2_TTs4xc~B>zy9{0|M;K#uYZ2_!<+Z}`=5GWeE0G1zr6hE&5tkNKD&DM>gMj*)phvxhadL)cZ(mqdw=u#<Ez{IpWOYhe|i7kZ$EwdzpLc~ez^H~`@`}HPv5$K`Zurs`tjZB@BVc2e*NRq)5L$VeB;$;AAkAr;WlTFar&IoS9kjlxA0r%>-u5;_U-A<Ua#Nz_4}K5=dTR@?&+)VKE8ST`j`8iy#4sN74b8hZ}#r(%UAn!eNP*)dW6#39{%3q0bad)e39c9@g3uL9{&(|ZSYa(ZC=0m{(Ltde{}v@$lh0<_m}<t_4&uerv^s4F!0CqKm81u)9+96;rEZadiLY~?afc%Nx(5Wyk-21)8}XFU)tcf3iluR)9vwT&pzn*#s1~F$@7nF`X8}sz`raH<;&as``ix|zInbJ)|);)dA8<{rYqbPbC3&@dw9>X&BbSk`%a%~`OXz9P`etO8r;<5>5pH~4MV$g)m*SMPrO>X%<T{C81Rqra~EbGJjdfvZ@a1Wr@@T@*X_}39R9$=%Fo-G#}7wWGFYK#IbuVKj|2AU<g=Lt!&7t_gAMERxFyba+IDmJi#S?*h;`3aX#Ld%4JMxD)B7VgXzx|eIM7FeIA^`kt9${j@9~TE&&VHsb@TS^{?+X-f7!pkee?Fszn-sNJuQLR#YRWkrJc|p05&7LSK!sQSdItV8-8WJ(8<r!Z`0IA2jn0uCD*Q%UCAA;y<qa~&ZF?8>vUF*kuUm?<N1BK@;syQEF*gJ<CB~o3AoO}62w&Caeo$Hz`S~Or`2*iu<*$@*B7>%$uC!Y>#ulRjyww9q>pu}JM1y2T0Gq<yu%B|f(>bL$3TwmL>iQ)um0io{mZ-W_V3^S-3nt)hw=Ezr%wlm;o)2L3@Jtl$IlBP?cx;%gS!F%!}d4L=E#meuAO(`x@+C~j2MJD7jq#mKt3~%iS4snfwT~~g<?Uur06|Y{~CU=zSKq|OY|DytI~(WpmivW?R~)Ni%DTJKu7+d$T@RP#m@x5kQX?L#~2Hnko)Y$(0-T`Lx;t|Rv|PquyE-g1G8d;e2P@TFH8vFfRm|bR5B8X?mYGDwRbvR^f3YsF1qHKBbI);&ey?|AI*wVN4#`Tmz{?)6RfNdHqo4EQbd}5M7Q)5am>>*|M2qt-#D1cV_OD9r8TtW=k{Sk`d}<di@-8T3cFzoSpL%w(~4g&p8$)wTH>>s-w1?#{$y8!l^PCF*70raZ`uB=d~j{&Nyf|)gOamg*!!SYr|7jGK#l~cO>B!rrCTd1Er6=InGS`X45>lq!N)*iz$L>(g-PnPl>i<mqdLYTr|YQ}$q}?K1_w)nV3Cy<$i-C!PW~7)EFH0WNAvRq${sBx5+9_Kqv(0`M90@{ASj8+0i5jk9uIq6g62VJUE_l+_oRYv$L(0-etyPS4wU0l#K2wqkq}bDV@Jz>#=S%ezRN>Y<H5mY>;+o!8ehYvIfCANZyK?v$hrM`qDnFXhp)2&9N)wQ1=>LG5!ML+$5%aLb3dDwY;)$o1wM71jU=GQ$X-*jK$??)2PxeqAaF(NsWIaiJaj1ogCQn?H)T+CnbJA|@&+rcAX|h%9E+%AJX;UB;=-OlA#jokFAPHT01AP{Ek?_J$Ow{5T8SLPw?UN2>cD$9dIdpdM8CirHsZ=VbU)Rzs3gq18pgsnGvv71b|rWo{0+85;{6Q=!myqS5LpbT@=Heskn<zD<$GE+2LEFz&ji0FNR4Ea43ciJz<DxKaux}AiYi6Yf{bHbT;F6>L8;0&v%+epyVtA4pU%V~TmuY^#@_{TAo#;Z?rVUWW||~C^X^X>VS=}~Kzs=>t>LRe1w}Cu84tv)TM#a31GjwiGWSm4wXu;Jr)tEVgyt7vIL&#3uOeB;d6kt!l;i`8*eDAx$*06?3G4^x9}2gWe;>i;04!%Kmd=6-_#r$>P0sq!iys$eeFqM{Izx4t`IcVYp+>6(=#WIftMqsc;BOxt<@%yM+oRT>h8=w6S7>-l4>1KVJXla>o<(i@DLNI8jY$M)KJu_YS0&IjMxvs(>j>Y;3=QvBTvg6gHDFKdyF!Gx$bbgw-of~XyLdcdg_;d{46KxtRi%~ct2ptMr*%hwVl`lGJZij00SOsAhp2t&!i06<Zn6K4htRu<u)ngw*t?sX`~Q4Xj9?l0EK(x*{nzQABPs!okBq@GW38QfIO5R)dCJIcP+X5i7Ul)XumyrSuZ(11<!y{5Mx5Cb=jaPPKut_$k)Y+OCOTt|Hj-s5U{$w<Z<f#?lP3v*qeEO;pN_fIj<hii`xj+ZlObr^h?8HWZiHZSzKJlK&W?}9ORnjYnu;?Mi6iu;Av__qf2$)>(Jz_o4khADdOBAZa?ki1hD80I?m!zt`8S^i^Yg~Fb53@9Djx%2cmM&`-Ac!<P0Bv&<II?pO6p?x*=dhQ+VZKahj4E$(U$=>fZe4uR4mf#yA7|bm6tvXD92S;`i$7b;059s*8i*zJ(MAaKTbNt?Gi0MF4DXUy>@I1raq0=Fx&01tU~GaX4?&}rFblwAtvz57F_k*fSfSg^neh}lXpjig-fngjKYr3!YTso^@!of3AjS<e*9@hGMl*=x>UXqg}W=8Bh_!U9oXCBBA)U{rZ-y9Yamr}5`c|qPLPW;T1(>%;%c3$drkqo)0@qDa8F-J(xa&Z0t97EB0IZH+6K$^n9ITJ2b!dKsEXuT0(jBv3MEo075=0bqJytk?Y+{Fz-t^XXEE&xX0=wnc`JX=4BpMxixO-`t`f3=v3_2!09n<5nU^#0UU(7xI2FIaIQ@lHN{x|`OlokozS8tyzQMO8Og{#D6b)xL(9ybneDn6Nk3}BynXkY4)NMJ9fea=!Qea&C+cHV`jBC-!1%c!`tqaDB&<TLhjy36CN)^cDB_{sw6ejuku=Aq&_?yj5pqNLm5B9BYw+3l=A_a@WE}VM0Su)*goC1M6iITwa=#)PzdQZR@kwhyp-V%lbf#}}$H#QqEE%v#rmJOPB)EH221lK?XuQ9mDF{AnZ=H|nm%v~rT>z3FtD#{#IVfifJXu#i#J-o{*(A=sjQDFzC+zUYR)}HI4kme<}lx6sUez*K&;O@>M<EW9(|BCNNt}Z1b1q__-XkHhEMY3EfE1kn(?|Gr;b<JRVbrT?C&yJVR)ND4)o?lUU<28H$hR%#@f5yc)z9{!8oVjb>(-WpF2+tA6nBa3o4X{QA@?MH4DT2@}#{US-U2Py`fUs^jVOEsv1_CPJ<c`1x-INH6*n^U;CTS-Eum+LeB*i7h><taK6gf)p%=j}z*_uy&|C~Er3X^Jb;+JV1+`)aVJ?28d4LIMdYkrY23DV{A{dHcgoLdL{pjMa&Oo59P1eCID!uoqD+yX9p2WZ;LDOqR4>D}VI_}%HY!Ld>Wh}g|Q9r*s?8hVsQql$$Ha8+nVtL0fG{fW~TZU~rE)*wrbr^w$i@eL}gqu{_{_5h24h?pXB-c#t7j;%^|tKG2Ub(@w4l{PG!rZ%v=OztS@r@h8b-Z6;pj|eu7bZ0j$29*GFQX|u41B#q$U3qOClNzF^7XjldLHko^po+8{Z*zKMRHY^tD?xjD=CuwaaKd7xd#JI1v_^1ziaO@FI%_vPW9ltCS-Qi3i162QfWg$$Ld<Es7HyV(_e;>?ZDBiWI8$hdLKe7u`RHiewuKTShJFQ1iaGJDll0O=e*n#b921CmJI<h6JVIp?K84Uz7foa9dMOS(BEVq+`a-_A92IE!BF`^{z3@&Li+pi4Hc_fgM4_M`C<1iZN-oVC!ek!O0uiuy&6Oq@l(`I*(_H8ju^!N@gV!Ec=ro$6QY{gQlE^8D{Bg#U3U)J%g>_>@8&d=6H-e5(6$3x48^s(LK@Vk@ZxUoJN6)Umt~7+ofeEI%ceYu+MVI6`A|Hfyuh8F0Hm;(862oA4c@W`{$anM}Fk4GtMVbJ3y=}+DX$HLW-wteCgC}#SS7Op*FSS&dEFWACpnt%tFKwq5YmZKg1_ddqw8PI`!1WSS98530)^rEL0PB*Ia;;Yz!KrK^Q6KnZX%C|Tk+F8ub{NKfsCbe#KJ&dsh@(*R8_ieqP*xcr3NU<81XSSLPZvI@k>@;l&j`c;)U`arZ#q9t_7I~w6XB2q^yK)5hvuX^!(sFJ5@o2@!TH+6FlJ@yG*NMd!cjBtfX@v6jfns=gY!<0rNBXQyAp3l=^(0~o3;5AUz)3Ixw&|I*|pR94<oI?Z}Ms*iq6EVm53YHHL01{#!N$0<g?%+m`tKwcM>)kT+O>a+30gUpNe#{tFXKPSfN!`>5pt;MeeSqAY#>C=#sAnK01A|9GGNQYpVFzmfF>7*i0ajM=STPSf$@a=w*g7uWkBy0LIvI@$FIldZ4975s>`eD3%IDI+iqg*8Y>KOI*2Q3p#o?weEOZ@rOHT_JY38CNsY5s<<DagQL}{9Gs^i0;L~4R)dw8{B-lZWaZTgX3e3Gg1asBAJZ((l|t&N3|8KQ&mC~4EL4UGw1%jeYsv%~8Q7wuAXub>-;4&X%1rk73S*<ApJlBhr)MnxmZ4}e;o<or8KY?At<hcR*KfYh%B3ih6!!#wMlqz~4A|J2p3ReRXT~6$TEu~eCfC3z!Uf42NEjw9QmbX%ermxPsyMuR(q<*5lvBhn7*a`#exFzK>%yBb)lC9S7`5%o;uPUr%7_zxc8*~vl0P_k1W1_J)YOCw3flxSd5LWhc@t<gGSEYA5($eCeJ|x@h~P=g7*#Na@1P0Ov=`US?ahxbZ*S(b|J$5~sQto#k5!YuP!MPgAC6BEH_aN(i+iIqh-WBi){dwt7i?7f*I67n46S+@Tvu1@Prl~7wnJv1=V?9W+2K=NkYgm$t`t1V=UP7=eHjo^!S<B}v}0Li=!&P9?ZILL&wjxo1@V_El)-IrJKkZl@SEao9bHp;5Ke#J?d&o~Rr0i}n~Bn?5!QGB!N*OO{`~)RWJb$&nMc8X<otJhHVd78Juc4*gY>WgsR6T+-ere(P+*IZq_D%k+dCuFy7(Y#hqajTkTs*xqjXPe=$zhu_bbQikQRCO#)=M{lD6Rt)4d@fQSi|eb1~(M+zB*3YlNkqvZ%U*T^9TEL=8%prHx311UkS}FGeGIjxnuFp;IbkMQ5fb7)q+;oPB4PNcHutGF)FBnl^-rzJxYeWN${HX3tliS}bO9Rfrg>f?hIeriDx0o==}BSu5fk(x?~|W91f)8mKY|Z!NLaHpKEXO>4Zp@um}k1x;=Q<(LxrV49~@lrPKSB5nq-%i*P*+$=MVDq8{qvo}_aB!k55`Az|byJVQ+$X9FAnvh38#1kH<oCsSADVj4v5{N>`aG}%X@g1dvMxL`9qzX=8;E0ND=XH*x+JNn+Ud@+a&Svh(o2N;NcRtMZYQ(I}oQ-8&cx#N#l$8#^uHOm4h7Ms^n#{+hXd0Uc|M<Kw`e3m~Afh&C@p`7fko%$>0E1TDMxZkQ``Zd_M|7Z5;50sFL{LkVQ!p@<NxSH2b2TgjL`}K}X8Uv)Mr0)P2qRS7O2}NT%HdZ7kOgNg5DrOCB7x1B*wN1IZHW?~2g)S85l?}^E;7>bIDVpCOC008UF4N*%D&Ej^NhSi74c+#oz55KjGHr+!RQ1eB+D`1y^B^6d7^|Z#R?P-5-EtJqfi(#aDv>BYj9~^X!eytKNyzO!)k=wDZuIm=GZ0_5F3xe{2Jdt&ESgp!pC#twi;OVLI$x@c*M+gN~dm_X+#j6iOD;sv0@hS_!YV<%$`tT{^X(0^TvWwa#0Qd?J?~=U}pQgFZP{lHA)*WxGK6Wo@RJw0i6e-Yi1TtRQoVNy$~Y2wJTY@c%HgRQ}T>@7RwkiF9i38q6XVOYG6+E8099kDIIJV&L7H@7$m}i;E&8HD$qysmHhO)jc#Kjn{&u|W~e7;N)SHEVK!C@@Xo$LdV{1VLmIx&2Q;@?oQ)-f^R>Fljpn1Fb{S6yfjuC4tzDWVn%|Vzm(emqvMd|}VOW~$Ym7F?G!w55sDP%^FkOU|CX!Ywbmxj>^ys_=Pp(qAUx0`b0;E8t32VXHm;wz>sxkA0vd|~hW#;38j1knm&Y0RsfJH5pOQb%o*Ez#)?j)X)*>Xq0z&)!>)d7>l39CRE_tCG;$bcgkXW_)4Ut!H~0AKaV#;moZ&^T21RhH547<-z)ovA{BEuB@(YPgBr21d0fND3D1jJCl0+<<EP3okO;kcHO}(9aWT4~4WEH|OlD=cBqj4oHgaU;DPPQsEVo@<DiL!p5bk?kf5r$)dQetd2l^%}(k1x#N6naBM1B61yzk;6^~v7DP6aD`}FJsw5}R`R>2}{_{A6D**3lD`Hb~_J;JS9LO`767u5mV9E6uHDs&n$7Jr=C8!}@Ec8^25!#sEoTHopMrHQMwj?$pH9Jb86Xsxv3SFj7Ju#b9sD2t4!ak{O3Es8_p}x5zkv&9Uq-A7b@RsV$A+%X21+B9dicTP(*O`5<fVaXKQAj;xL*T)d65<8>1l(ZSJfqzNT_{y{A^1|LD{w+ulfhcRmSO6c(9O!rO(hdTKyN^e<Ql84g2;X9p^On8!aMC$?mSJrM$4fOCn;8k!VXfA#PY!e_mkcEnL!HhNp%^$GV}07n@;9xkXX$Ow%$w)2~p-@b}}e14cOM)5v+bL3-G98kj~P7)W!#DuzlW61%w23C9`mEiD$s8=mkiXzwHCYCb?E=R!LN=-lpX?H<|j#)E_v)EcQ)2E}Wy;9Okf5r)g7e#8Qgm&?L~6O2O8{$TsHzg?Euy3^W2qeN~!|?P{p77AF2T##jtpG1osrQ^hBt>?kA00-|=80HS(oD=-tzDM_;=R}@G&MUq7|iq|#t>pBe=62nkAEogNT!eFP#YZcJRNu*59D{-7!W7Fm<Z41*?Q^DZGgJ!n`LaPgerJ1=^d^gtW*AltZ2*K!)AUY?Ud^9AqV_^n@@q(g4Z?aB4QAJW8h*Au~&KX&N3z!<{vRvglp<5ws^dIY@uEdh8nW_7tsxZEmNwiwfNZ$13Rh9?1*s><|y3KjfpfC9APzOEv33C=loRwZ7!41iWB%04O4YyLe93z>LoF<~TqJ^>0eWet3yG>)_FsHA>t3MtEsyW}KEUHUyU@Q)t>F<K8kspl{236>0z~Qi;C>WRG@RT4FXb7h8!(bsLv}#RR?*p`V&b=+9w>=P<>)&67;F|1#HF`-h-wyld&BLK&yg1*Pcfo<qFCc3}zh$fIxXh&m*!Lx>*lc-!6U}lvIOy{ym9!D6E~i&H{!@y2!*$yBh)6M4=R_o{*G69iD!r4$q$*}aSQxgP5GTuVfWE@8^~4){GM?c6D5!Ao@FCHRvD??Elb8G==j)UPwkc_c9HuK7Jv3-0QpSMCN5vu+ca-KyaA8l2_O&kZ*IuH1eUeG@0nPENtQ)9-4mka7*;JT)n(iw7zJ~r!k%m`jz)}*GcUI#&-q#t;Z<O`8C*@@EI$&S4l3Q7T$&@DMqb+=02U#PqCcJY=H?Cs1b|Qv_nS8-*zg3URzjN)j;DKE!r5anwhH_8*nD8ATUs#xirUaA8Awq&R;gatR+tP&67lBmaH6M9UF6o%F+Ii9ll|n#YmAGPeb=XIgl%H&{l?Opb>(82)E29GE^swndBJ6L8;{qvb4E(;Fl7_O-CM_{%3-_d98RlN;cH4aFkHumL(D4g&lP3*snQ001Vym#DGiUczaCW;dn|Kr^QE{z}7W-&SA=#lBF@>NnfM@j05YGs32by!k?aK9J&XGF?%-|WBgH{xigCiWBxr0d_S}75BC6;DrCPgHMYObg>NWg0iVc^Ig0!BltBtB)o!bg=-*217A!^N#aF@2MAC<QJTy0*|W-C1KnNmSkxT1b_s3!)VH(Jo-sFd#*mXGYb4nt?wzXM|m33PNdks@RI;6)6jBG+h!f=}`7SxKx1iGK0n8DXf|qZ_fh^0Imj`HNKpu);4p5-O1*xK}ArC`%UnLk-_2_-k&5!YOu7Hhq=(SAAjVv5=8QVdV`yKHH85~SF#XSl*S@?4RT#vq_2C!nQ&}pXS85)l9biA%WBu&;hK7CbmOR9_u>6k`&pr2a;0!;QWmP_9L1c3m_tr4`u9KVSq+>ccm-IZOoAS;e|z&2sHc?is0EkliD0K5bt!Lvd*X>)-EOzYWTFL4O38w5xTB{86{>yoiPM{66kF)pt#O$Y!ZoAa2eJurL{Uojz=EKIITNl4l72>&U~E%%XPZ#=y8k<`_RE&GLcg0`j92ox-1=1VIl>t&!IHMQ;43ihe05N_D`Ayg&A^>4h~Kf)XB^-aWH(VjvpMOm(<)gY&_p4D%_pC%1&qm;qSGj>a2w4T@I3ef4@#JOj2db^Xm9kpa3@F8w;HtAXuJs-YiS}p4n5qKZM2{9*m>d_Gg=|M;o6kl!YA;_aupf$tORVnnlS*{C;cHaegy84TNW6@Y$C=TRnS^@1(?m9skIU}@vsyMLnO`7#*At*SY)QOG3DnP<ziJq01*Hxi%`~7k$NOShP@XLn!5GV;5HvjwB^j?s-%3}IcJwX3Gc8or#u!LOhc9tj<Ty&)G6iHM@~OtQ#e827%g=KX(G%gQN!Ul^<_y?m%yfUyVmeLuu`1h0{LGL5u^xLVu}t^rio6p(+8B7*en}UddZ&u)#{_WU`Bosb`%w%spWrkf^iPhNX|tf_8nw*ih$^5@<~DIEY;xkCV5XG7v(3zmENNRkz4bON2SITd4x{Sg6LMgNYBco89|h3q$_a{k0qvOqI;zNXzYG78oWS+7)3}3CMUxJ4aBuOOIt^p(=e@$49@9L!c0-#i_U0MCd9?5vVt*FrE;2hg2Yh^fP;AwvKQ+_YxeNIFq3GSgcX$<6Y!BcI^3B5L3+-5MwpqFqGSo|EQxAn&|ZYMWloHp7xwQsYB9lMMA77e@Smw3MuEA{+c^!mb~T`>ww5b1W|=|R@Zu{JgwKh7HR;JrVXqk+tB59hJWu2^4rgD~NC*yEyI@!kxauSpw=F1_cr`dj!v8bWWsGcG^zezJ9x*R>LZ21p9P~=AKg~qBp8uhpfW5(Y7hz-Vo`!qHq)#tMy*kHn3vGT%W;=i%<5a840KfrIg350*W#XO~R$QPNP#l@=ZRmIPh9sS{tTuzH;xI2J;G93Aj)pZg-2|d6qc+ATTJg)xl0qD(7)D@@)2oyTv8euHLx7c@R7;A@m8iBAN49`{)drdl=3$F|iSc+^UU+Z!7a|D&m+=YAkPGruI}WB`t%?(Rm*?o#;KUidLmt#BF}%pE^wRX$i09}KmKy5xj8I6oVuU%fud+2WEN<GiAzAKCS4^jvY?5<QMqH+WdB9Lv6DN!x>`o+tW6VI!+3goyErn4JYmiINnRZxn8w~u?7#vA^NF9MPaA@GRBs4!J_*cV-lBOqvbcm+;aWA`}5aXfq3Z&$bQzTH=ljlTr?ohYGiUJo-e&oxfcjh3Hs)Wlzw+3&rU!t@&3Nvj>Bli@9O!cxnF)gz%F;bMK!)1RACv5x0aKeHdc^5FdG$m|jIXWB?c?7W)N$~e~e)s<7^~YDYXQE9{#T_#{JLmAlh&t1k&JY`!x!vQ7fmiSI#rg#A!s)u(>kg=p#5TN1Hcy-kAhc*?Iyyxn3IS~x;nCD#Lj_oQ0v6c}NSU@d?_`g8Z?rke31fx7)x+7H1EH#!{HF3igZ@0TWWP~exI?QzC2AU1_Ockcy^U$8N)6DpzKbaN_+#jl53rJk&b*yI3ytOu`J6mWY+wLyhS$xnH{>nqSvW8<_03CMr_$yqno;a`v^w6VC>Ke&C9{uGResBYa@+Pn0;z*Vd{8ZMY&Vlm%GtOteKiOv5@xC^@d$3SJ|9vLTp(gd1yt3fNP4<P!wZ7L13#Td1BLk|mVQ>I%vh7B2ShK6Ugv>rbb-M8vK#n8qJF8^ewti`8#Qar@$6c%CLB`ajzF6XxLfYzS(SV$eD^iBmrDS8Ji?R2H;JIsM<-6>xy4sIUJ;S-Cb{Z|f1wbVbnM%f*MwfAr^Mg73UY{qzcta#7t>Kh2}2(z*YR>|MzJDm)7~Nk*25Sh_07k5@ZsqS+dD*t?Ks!cq~X)CmXx0&IB{1~@F8<dfIrnwM0jgtu*OqL)(eDh#)KzJ*%|=F4w5CgN<gtDCmEPwn#cJo4OL_;C5HAAkXqz>j5$V6#AZff(`zoKS%V~+nq-4*S@KF&m<Z_uKE6tTjHcKLVBHj9Y8Q9qN6)!xHfbpBk<JJ##ANlMyl77PbH=1zAceJM^U3e|L_oP5UAT*NXxCqnqF;xHCU5QOgl$Ksw>aJd#YPrDX^Q1-+N5nh3PuT(3yCCirtUG{nyt4578IOr*BxZ!ttkO2ac?3a^Y9?<=yB%Z6|-jeKYJ<%KZy|(T6ymH3+4gaVQl=2)3xdMreYEaovOwCJ6#^H?dUVY_YDO2j148trb=K9O*+b_QF=fgjXqYpI123@esA|@VC8K}t*e7lZQC-?`LuMsf}S-6mLx%MH(SBY)j;?|cz1V%ZYDI9d0BRpUT4ih^_;8nU|m|>HgQ~ix*fBkz1t0K>W_!atlPx`Xm>rTnkQ;uM^ZqBVJ08Xz<~kimzVO~6zb9}yw2c&!e}j>T3s@uG6=5GHF7(120n?gQ7lyX7Qfo2=S;LXWleC2j#zJ6YQ|EmUG~aLQW~aghcU_^6fty=QZ2^-SnZS~7yV0*po3_AC2kH|=g4*!!$6o-_Nh6AX$`=W7nr5q@iIF$$8i}+8q|Q2AexU;_na9aE|N+8fZ1|NBdAM5f_@DfjT|+}Zu8?26KN?-vrdPETMXyAgCM#B8l82H84ZIkOn{|&tCbgJX85#}ayIXiRpi(#l*-g~HQ{qNz)%JVUiJ&<Y%vz!!xuAWCLDe*k+b=-xOJNgaq9-Kw+6Y6bF)rvKK}lIgj_hbbGdWdng)}Rua|`8DjM?qt|-uKu$?(jgo}x`!JQnja_d{9UhL{m&qV9azkUCH?{99c*$dc8k}Ul2(vN>%H^Z1S5T^q~z+wyYrh#z_i;X5fIIF>s3Um-0*O~`Mg6{J<xitKct)^w!xxVTgOf{34tWt%Nq-XH#kQ}Fix25Nvk)C2JwV<~x-e7=&BS=w)4=Kvb+tY_A5ADuXbFPeVaM3k7XXDPCtjDkeq40VEV8FD}1WaZ1KP`_(CA1f&EYkSyn3r5T%xr!Gj|%ij3ra}NPMF<_<za##GQMU_4h*`Uf<PJI84BmTQK<tRrJP6Z)77|}V>5*rl5l6-Ovw#&G-Fk!6vYfi{Z1m0+?YDVTIf2CKm=3WyrYAX=#|pq$tqW)PWD*o-Xz9tE7FX-(*Zz#;F_aO)M=2|>4Bm6?#Tx!uro*gSwy`^d+l-tC-*X4tZeh*PeWLfK+K5rlYyE&&A3s2w9;Ksfz2bRdAe~9DL|ztyn^Ryp+BKgoR}ej?rMkMqHZ{1J~YS{axL&}ESst6hoo^Uu_4OQW4F7yK5do#Ue9um8RIkXWDTIjs%t92X?Y{5s5FJgX)@n1RmxCssR;7+<#fE$kUyn3?T#Gu$XH#Qr^xu0OSsMMgkQyBv@lqf)3OI+tLz$)A5kK$XLa}%cGboYpfQoIzQx9Ip+T-|*E(JmM9zl@8T#Y^_$`oLU(}Y0Kj+CZWWYHd4E~DMexR<xqP=nQ38nw|Dpr+e^h*JAu8IVDwPpboCeQAR`iy7Yk74pbqn`|c<pOCE<8TWUnx5Jnqoc<IVD`+)b4njh>nFO=QpzJJ*?OXd&k96TBoBm>aPL`3vo?Y)Vn^v@Ds#2HNd%HG1^hJ)hn_zjPwLV5D?F*7kY&%Ql;rsxqin?fUKi&PL2_hIsm#kClEBES#rzg^BZ?38t4#Fr<Um%}0s6S1p4w&P1_N_KYYi&Y1x8=3?$EWZwHQye7`Ll(#^pkMvG<{Sm6Lq3ue}oUYWL{%R4=5ua}-Ns4f$48lMEigHhds64?kw#=t2xF^9k90F4oVgXWB&;8a%StG2UM_8T(;dP|LB1z7cT&P~Y~&m@okyV*OKvDCmg60zyR4*4914YR#4ns{05B;P?zkTBY<DfQ5<&TH!sJf>@g60Wb*gH(e*do-2G+d#XI!R17r%3|0nJY}{x9ya0ZTIwSDt(L`@-UblbYfE?frr1G4a<9nAim|SzMZ+6~xI(;*7N3WgkE)!#}nKJ+zb+0ohG4kTB49Pan4Tl@AxqzbbFpT&u;%nu@FU6k@C4*g}TfHsFAkeqsQcv-3n4?%R(i9@JFQu1^rW*hXp!Wgo7nn+WDYPW1z?K0#sLS7+jMyGRVAD5bt*@Jcb}N)@TA&a<W$13pV)-RqRMfsyv|DI-GcP=UNM<=BV&|j;N7NwwliYNr=*kluK%?Z*rZr5@t*yF+ZgF--+AwOfr~TRSZV@C#gVLePa-3)y)6{YOP;88w;!v71CRW|c74djKJ@x6UE@aRayK-vjya31AvlJr2J^Uf1`Z}_szcC&gAXYF%U=8c$)PY*cBKKPU0(epuE9&HLvrWSN&EP_->(nM&`3G}r6#8hW7?C~lIQ|Ka|0J3t+oR`hMi!snCy>Wy1D!HX=6;Tp*ya^M2ih94Pa88BaINQ^xsMxZ0r3H1&rywYd;Ir#BdJ;T4%Kxbh#X!n=Io^}QWOY2|B<}-P4xd8#4p;dNl1<-h<N0B!$18$bV*^X')))
_PLAN_IMPL=make_agent({0:_SCHEDULE},**{'hand_align': True, 'weed_repair': True, 'sell_lead': False, 'budget_guard': False, 'room_guard': False, 'clamp_sells': False, 'dead_stock': False, 'terminal_liquidation': True, 'front_run': False})
def standalone_plan_agent(observation,configuration=None):
    return _PLAN_IMPL(observation,configuration)
standalone_plan_agent.telemetry=_PLAN_IMPL.chassis.diagnostics
agent=standalone_plan_agent
kaggle_submission_agent=standalone_plan_agent
