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
_SCHEDULE=json.loads(zlib.decompress(base64.b85decode('c-qxnO>bODa{Mnm^RR5TI2_-!n%)_~n&ChnZmb8wVgavVz*ryFz8U`S){6b{`ekH9WL7nWJq@Qx^{c9vRh1bT8Ts4)-u(NY|Mu6v{O#tSe!Kbg^@k5PpKove<In%~Z~y(}gD*e+_0NC%&%gZ7m!E&T`TeIq{^{5EPd|Km^YP~PX8+Uf^_Ty?`h5HRo7ca*{rUB~FTZ&6w7<E%`~3O;ZZE$2?VEr8^y~T8*+V|;-n~12`(5_!>yJPDwA+38_WQs8;-|OocQ@>Z)zE(b>Fv88{`6(;A3uHlv(v~Hqdt89*9Y?t&jXBq$EUhpv3IZE><(XeF{odj-hce*>vYgh``w3+H=nIV4KFi)YllC$zZl5#qiz>JoQJVmRKt?O!~d|`{ct(+^_zlEKCavIs?S=9!-JN#arvBEG`z!x`t9b;YkL(AL;CRd+27v$ynFZb%gyaZFV6ELZqdM2FKRgqIn57GpDrxxHh&FqdgV#14ek!V+vh!T`VE=TVO5fK`sL$kbgKt_eQ~9QT5Q4BA9wHhBg#v){-(u)537hrpq_VF=kUDaH^2$TX`O82_^apd^>*LoP+o<puWqHKJ(HC_{7%jMPCt$rN_nM?=bgVZp0IR%drwQg8h!#6)n2~vEw^#1r5$(v$LB*T8Yx(*WN#e@c)i5|yJ~U1f>n{{(D9$6F`vIW{8al!@<rBHzIl50ZujQnpZ>6W|MBg+xBq&%2A4Km_1=DX|MY9cKk8f=XDc|~=ciB5#eO*E7PBRu#^!V7W{Ky4G7xqF#@T=uRoas9O^4;0U^Ghu+`T@0`{{?HpK$pKI!@@}E8%n1WY^BjreG(R?tn2YJmrf;Ilk`nrZNHo{1oEBZSwcA9MiKCGi`n1Ep+mdPLJg40Uo{~o7nT(!Q#+khAfZVinR$B4x!HX0Z%_TRq;4l{Y}a1Ad5NT#DL+h#$Ef`@FnLT1}0Cwwln#)KXP%Q>XSTvVLX%k3(XoHaM$YJdp_yctM`xKNP%EW`c{*?Er7}}fNI?TQXXD%mq-g>o>%(2l8v3l4<-UOTL!dfw~}8yw%>*#UnB0>mA$Cb5s@3y98gg`KU*3Qqz|n_^kP$+t6sFh_YzK7_6r!dHzo~HzPPuuALP#7uH3N?AK$;;|9<!W{U0r47wkZQIMJ)1@c0M`oIE#rj{fxe{l5^q@JDd|B7X82%hDUb@v>h0kvjh4jZc9%z2@K>mkSI(Y`IdoTN<2~i}g633#F$qryZ=^X>#))vhbzA?56q5#~;pTXvfz#9x!s}JKrCTZ`5_2XJ=i<w&*{z<l_stx&Ut`u3zFMcwTAdvz4&B^wzHAhBvcrPUbIL17fHT9aUVk^Yi3eLVm8=;3O5RoXGr^CC`i4U-Io55=3rIeY%UoX0>Iv!k>k1!>9q+>vKlPh$oCr$l8s0e93Ud(2j|bg}O7x7p)LCP}i^$7?7JWf|p>;JJ4<KTyrmKYA#LZxPuuE*=q+*tQhMQ|7Z-%tvsNEZ+?RZXfM1L5V2RS?5*Lj(ug4&!K`<JJk?I-orDPupnJg04i0z0&E8H+&1>N2zTi!FKu_um0>D+KjSC(ym{xq{9xzQ1@pRkw9M<#Ktx_}tiFzMEm5*ZCcom9`EX#SU{<7F^sE*+DX(!Y2V4aA;cxGAf8PVO*d@69KYXq6ZLDZ9DJ`Z?`>*3J}S*M841!!^1n0Ij64@2Bpa1&R?XZY)t;W^Hbf7*6@ozcac<i@0j#<<r~SU(#E%&9roKm$j7nHu0T#fzz7S_J&ej@TZs=Odo-_H;%e4|(7KQGcTLJm3?ot2PY&UIk;Z^WE`8k0HxMW(8oUNsizcwq&J5t}#`$;1pE3)<oC5gDM#=p%gfCYCMo|8PPU0QRPj^6LYMl1LZh#yB6?~`(2a$qax33bP`uurMXVu%YXlDbc@>2ZX}C5$&SK??p1?sn?9uUDk1eItsl5cKdg~3OF3v(U}Qel;c-cxDaiWV;@ZdKUtLgj3<lZ$>FLXV9zGZFQIy=24r|1c=GEVvzVfs%$tX|;^04Uqt`5s}*fj56|MJ6)22oDW(2lP`LqrDX)c)Wp0I=rKlsAZR3lIdb9YFx9Fb@DaH}{`?V*w;oHWq`3yRJfAui}qSPak&8ntyal92fiay-qT;LPi2FcvXw8<Cirl&4tg#mQ=y>c<pkV1U%)cZIZ!z+bzb?XTycliJS4+uHHNyj-yyG5>MyZZzj$Hpbzn2d;U6H{+`-;To!vC5W_ZAUu0fl^%_poj@urr4Y~+qbP0mIxU!*=^tj8dZ9s0#VnSstsB&5;&Zkx6PGDfY+(kSV!^)i(73@Nok05#hLxY7yv)QhvTM-=K%lA{P*Qd8ZsyncHu_$wU`3A~b5#*Fjg?_|4&8)F2o`E+r+Yc8Dd9k%Ywj+Nv-B*16DUw8!k+-(`3(>cWVC7UHh(^4v@1wk)@U}!G7Ctf_T@3Ac&PS#w(g<o-b?Qr+7DntL3l3G-3Uvk;_|Qi58R5B2>4@GX@FN<fvPK#yjZ+Y^1egPw%Wku}E2VgHVyB^M!nyCGZ3rk>476g1vV<4G!P8m$ww2p-CF&T-e}nFgCfo16q}3AYtXUBR07Q(Wg}hu&Pl~3>%AE~X)mSx^#Tjr_b}-xP!ijP5xl26j*767mKW16)k-7aW4PJ-fZfRf*EZT(*2pwgKduRe<QcPQgJmi&03>|pp=x%qf{^pQLBpd6o&r1f*XwzV7hN0u0vorWQ7e}Rs_u|9}hea(PoS`~<D}!SJi$=aO01&LI2yB)3-Wz#Y;I_wY7B?jr&d|fzwkL<*eo758D&@$hKI!!{<_5}s@y}-Q9zo8f_!AieNGHEsO#SoQcmMn~nZ~1OczDkXtPj`lX)u{C%zZu|n(xggvaKZ~8&SBv15`MAvc8L|MMPwMp-4L3v8Nxvo|zmgC#w}h1vHeQaJVgXsqm3gdfmHL2^-?LgS64bs78$vTy7|p(_y#H;1~FTZ$)&bp-T{5I`j?!pTq=U$`A&P23N<(tHcaV?QDI$szn1nCN;bY2a@|6hJKb?9ndnh1Tb(F9o-Xc%=irEbo33E_ZCe9W4f4GmatX}`1thm>yJ-G?RKU`nHdOBm%6nC)F<e`L%AyyB!tl*OpoDamRdzNa2)7Cu}`H?0aZ9`Rky+bfl)97knOHHYOAMn5Wp8S4cbt<V(`*w9N6&DpaykUX>A*^>|SksbtpX3`m%cdQzKK4hz&IyLF=b)NW}*2ot9yfTNLO*ZLI4SpAUHLE2)|j`61_!dwO1M(uSAv%);G@T-ky%w9`VV@o&~p1R(@(DW{nyQcm&5d3VIn7Hb*BF|PtDI^=P1fJqU9%SkcJyPk=sDsYEicZYK?1I11neq|(&m?}lXBS6O=O1-a)dzd&J<kOBsD&}2)<}_L2qSbxyFd3(`55PMLuP_KVD-WWzON@}DuzMIc{t($%tB}Wf@SS%leQ`5Eu35Z>REpV|qu5EBC4CMRXKgb{`~}9wc;EQ#$2+G?18W6tYl<)lbz@$W_s&{_J^fc{%mghn^5NAbjNI#`lfdn^4g+YUD2|NPN}Q&g)K@G_&HxhX^NH`l>*kh++M@Cz51jjFdfyILt8Vdi6RY$2M_1igVd<G2f_NqV`N9N|+vNgQoBp{c8Qpn<#9OzYV&f)*eUT5gWcG99kQ(|s4AhREXGe44T{XR#Pz%y0$pmPYnLPE%s-`j~{mxGt2PH0+6G*-T*tR(*;PG0}(j`OUo(78Blv)5kOtk{GjdFy-j3@>Y0S`|ez-rtn$Rs3}{S}tFR6E$_1d-oWB1l3iX3bo{NAU|ZxN2)WDIIj?YcqNB6dh`&!&%#@WDfWmf$*By1Ym%#5rZk5-=O#!Iuh|Li>eX8kYj?}Smv0*TK*Q~SIjJ%FUzVJ0D%6_G!M}D;)G{Vj7TAXBKDle4e&t(hL8@$$L^^cD;WaceO%a-5OSZqlFRQs%-RT>qhs}q*Uti82>XUm!%uGoLIT1uB6O_hSM^XWDR@<4j*I&tlB>=bFeMS9uwZr5jm*0C-buUn)cj640$61sP-8-RK3l=rZt}kM)pb$vHtmC^tOB0;%7VDS1+42}84Wz&Lb13>$8N~F(i^?YErHDfmnKVCIxA@C^4|g0?dtE(x6KaJfel-%)}Iw|ZVJ%BI{Oq;%FB4Bp<Li4GQ9_)I8xB|q7?{PzO9aILBXn2!h(tI5KAU2(%o3(PH-_)HeqOA1e?j1><B&0I66@4A~a@-(y&|--LvMlGPDGGD+w_%kAvp<Zk5Z{h3AX3u)$U^_Z496?rJKTNaV#PUkOH*Tl}JnjqW>BV|wS2MX{^b+j}f6QF9Atz5DUUzhkB{T90U;RceW%@?C<BImmUhOHJ+L3s+d66!O)@HCdqrHH?Q`v3`0Q<5=K@a=KlM$igbaVA03Y!Nr)M^BU(S+{uPVFix!Jl4LLdyrJ7bBPu=5y}8c-T@vciL|__&juBWRo2Le;_zXI*3v;lmg)wAC&X7-fFxAc!g_!cHuL3{jj68`Q%T3sCl*Fn}RT?{n%F^hG8d0+Upd4o-^t3KxGpwV!9D8i`i~lPhrVyrP=zobGvv6FN1I}ZFcGP*n{t(-X>cKJ#1uvRFT~pLyhw#U0KV*FTQ=aJR#WvsKo@Po|DoGI+(ffyE&QHJ|G7$GR#|msP)Ff}os>2B{$wOj5BHYD;B+F>Vo3iT~k-J1SfCy7)>gv-ZQCLJsSVv6g<t~A99=UjyUvIyREV<+wRE2%k#i42pSq58Etqw<k;sS?QKn`02hNjQt<(74NtX^`j`f=&#0etQ8MJperKn(m)cDSG%Hr8z9#L8++5Ew|zWP@rTUI!UVEU;Q#O3~X?aJASFN2OX5_f`EfpHqW_AK5WxtH^{&{Xq>zLk=^$%Yj3-LJlbO+hybtP_8@Q80Q1Z5FrI6Z^`OGE-G9TVxB^@OxYAGWT7{SEmIw#Y_Q)Qxltsx5Ii+`J+|P~M#HN3Pta{CjG)PikM?JsYkTJR`Q3RvteBh_1&0{MiS4ZAvb;I7!rpG`wK1n~H$EV6Be%$$>W9Eh&>EnH0$eC(q=o7&JI8AW1nKxJ&xN*eCbBQPYF7{wZ-UHch{212!7{5nbYccP0|ZFW!7L(!!x88dgKLTjmBw4*_=M3g2p@?Q^?h;UbNL<#<F9dh_j9ul{(!DC94p>lF`Mgc!?`#bV=p;eG+o@e>t-aIz;m&3lo#b?F5sNxjl&qj**Q=RK_OdRcmk|M)#Pw!De}OR%#x^sKV0z3l*=XojqYO2TdZs=D}+&6Y2L+NrA`aXv~7u*_Pc9AXQT~7xt{Yr{YzG}L;%#KeJpDqV>RR<8usVyu)F~8OGi+?LaGT$<`CPq!^I;NpHjour|KE)XkUWOCS%`y{k5&EqSxG7P=0j!mEC8u`jZ&{o^a!=94Mg&Q3^?|C{X}D=%Dv4!1Kllrg|xvHikPeq*vAC=EI%^nK;KNq?BUl9T7%(blWtW98$7qYT%zSJdu{yy%f|_NHb8Mn(G<Z<tr}1hDHcUxi-;C6nkf^tefuI{9puWabQkmJ@DXNH!<pf5OO9B*Jq*d4o#{L7*TV_csBx%m;_ERLg5hHT-E~El3QXFh#7;WbUqBA>`c9U!S?|h#I3*uAvHxC)V*Q8oNKIqhTWOC1;bP6PPiJ*l0bD7zh@b~8Kgaiz?kei8a(GyA~#oTGs>xV$qJipg2fR(EZ~Fn?p=*GE-QkB^sgY@b#cnvWhmF?TS#~HC{o1j6K&>K42=zibU>f8S@K??;Tu={GK#4XRE^fol9o~Z;3&<i8y$qu2>aG)R@=r;JZKnCjz-E;5TjW6q96_sPs9%^4a#il6=@^DuVNCuM(&lPjS)Pl%RT%`TdmQ%7R@9pmh`*ab*yyqmcu@X1b2+C3$n^KdIEAkF%Qr$jkK}#TDhFzlG$zI_q!qm+rrqbZPh~F0LGVUG2T{mk}OCJnCk?FoZP;dM;gy@0CBVIYBQq^{Z*4Y#?+%+IR&F2Y(N1Y_0BYb5E#%qKbOkI40t*z-BfTnlb2b%8AXQ~-S&jU>~*&&;L{c~JmLH;DzqXa;Z3kt6qjoe)+$*$Rq&-F?YXQKj!Xjz9>uy9z5;)~j^vdM^{}h~L#^c}Q_PKs(&|IZhI@yN3tSMCgQd1flJsEu!#arGxNJbnQD8VIj~&ZQYlfWN7v<9GqHr0g&EvAVX4kfYsAaW=uf8#1Dm(39k7?E(zL4LOP})Oh!X(9ia<ZeyPaU!tV@Xx?fR4+tX}}Uu<7VlslL`lmi$W8o$j7P6n~fHV0DQD9Xm3Bupt|N<E22l|tKyoH`$;g+<6=oZo?Z6ltL}HpHhVlArj?hSpfHeB1z6*J#DZcWFfSV_!-6Rp0?LlJSM9PX@I0n`s9pSMv0W)M#q>x#IVSJNi;56~$RIVgH;czFh@<j&I5OqG=I6bLh*FE2z+(jko--QQ1Spnv`7GADW!N60QnGVl+opo)ctw%w1p7|+|9UY>nBsCV(P-cl5D&j)f#xg)d%`+B<W_{|CdQFgb!3$SMe5W>Opyn*z|brKd;YC`B#WIOX3>(pqjbIRbS5Gz>eu?81;}e6Y-Ls-ck1a3rsZ6HGE3KA3J^1;4?pdcKyWCtw4=OAB0s2Wj`KsIq~ul9gJg<6T(s%jTPKp%>a~^+0WI2mehE<SyEY~@g3ocz75q@8mJFS*`=GJ>;iuj1*Mkv_gK!{ie0acJ{^14hZPUi2Wb8U56h^o}k>Mg3iZBXAjv7OvCZcQp)gXB9zQDUv5V$9l1$>wWgd=BzC@8oPLK8A+i6A4I0Jtez;9bSnRzk*>|NL3%`OAU-@e>#qv}~^iYVWs$bQ=sFPnPG?29I92s%e~CLn)Q1`;8&voHQj?D2El)-!86a!`*{y6e8}#iq3?X?lh6+1eQJy19S|PoE6<Yqg3}=s7pjT<vtafHI4DA6NNT_fC7AdFt;F?p0+|FwLpll#3I?dk+ql{RSSM^lSa35JK3b}?8e$4Dljim4sM6Umhc<kE*m<^91-v;r1r&5-ambeue8z$00{b+p=?5CPh;4Ed9IwMTXoa)TaFeyShvs-G9Szokje8`9VbxfT}E4M=6UvR7Q^hh4ndIdHaT2)&(q+l;zm`zHK)51HRXL#8(<DD<jFH?s+<Q2B}+O4{iGF+kN+TqtgWn@Pz7E0-<)MNA^IL^PpS3qUyyV~FRKBX)%9srnZ<UsuCm&zYOw4Ot0b5x+=Q%@ssaEJVoL{8P@MNU_{EHVr53$Py$a=ftiiw%%w^ar?Cnkn0tbgZ+sj!G*Xim@mXcb9_MWglXmmKXP1O0J>IKVPxlN_4xq7+YO8SyTR{013NM@H9ssLX&@WnpfjMtx+=R`UoT_UyN0XUVnVw)m056r31cNk2;ZqjZ<4YT<h$ze=mV&HZ;achYvZLvBNf#S=L0aC+TW*S&a;S$`t&N|=Eu-&ja4vY)q)*@xSs^64(!6QXBm=Yegvy0xgZ-1=&yat&TTUJUyF-255{6~&NIPGRl9E4XB=HEMG^|OT)xqs$L!Z%0ti}baiOXVoA=Qk>K?h3N*R6)Hbx#@MQ;LW01Z3rDI(#!TDtfDPjU)9H;BDKo?fI;vL<#$6;@q^&>xa6y1H^P`}5_}LD#1i#cj^T{-9=uPwM3ztpUbid~J3fkHbXv@^as>htO<j9UoNW$AS+Iy-D5U3I;*={sa;pnA0Zf~)4;Ln}cujFrRR+iS(lP}v1>k7<hM_>E_{Ve|5tSkB_=Yswty1m^<P<FfM8twt1)K_yxBcquj|<YO+eCP+h-=jZ@iVtq9OR29M}X3<^=q+48G7z3W;Ztt@M5@NRm6#j&YnCd_!0|TmXMxU=nUH}px#mpN%BJ>MKI~cci`2_J)>y*rg-ak8(yYNv`gu@-Bc|@6Hz3;)7m1{8gkC<Byw)m_9dEvEA#UPpmk(<y>i)Ku>g_XJg42*=}rUO+2gaGzjqo<F-{6xCse%OEJVZ<%!NIt)wW}8<pwHinS?sFQ4tFl(l)HQfedp=&9CKA*i0~Br(rQF6@rquuM{axrE|6V10Wb*RvNmOH%5F>@c_xi&ho>MT?BDK*d)HIAP-t`^!^+3!DQW^iOD%iT|-j#Odu$@cTI+it;Qw9YR$U8)2TW{21{!IB>{{>l``^r>E?z2;5Z%*MUI#+UDRl9$e<1)qpK80YuZ%?T`Y4C>^j028u|+Fq8hx33aAUIv8j08-eR_pt8{z|sU!l@u2SLOxfSzadu0U|Bin@cMI?$bWDogT?hPP9X=<tX+?E32F`%d-Ycq5}*izCe=ZZc|P^(pGli>c0XNNWA_^B%@2%4=y9ffQ2&@_n&b#U57sF<DrHwxsESOt=tkkert(av3H*2klf)~{LZS=|G^-gweac#&G5H4HHU9yev44e3sgiE4sM4RvAH2E}GlkvR7T9T{+0x?@b@+2r{?GFxj>j4aP`j%TQfTKNe|%gYC_GYI{i@y!+QcS(WvI(n5_nr9V+^|Dovsbcp^v28hbZP44Eu7jnLGg{mY9_g%!qhGl{UIclGX}k=u<<ws|C3{;}dQZZ7k8=>Nb08Lgt&;3Gu&%1A!hHeP3JHdQ|M^l^9Mob8=Cm5(1;DLH4U}L_FL2}q=#9`^jZ+2JK0cS>A_TuG(SfY8I(%W0^c(nycSIkS_IkGc#|e_fK2foledBEbuTWnI<9}Ysyl3f1*h$;nM3i6yI@Z;tqA91Su}ypoS=VMlq-W|z7>x7L`$l|`-1!B6UGME;x|E&3rnX=9gi%;%ZXQ99ad|X`Il0aYWBU-O5EHr!orn4&P}o}|C^(l3@S>qM;W0)vDxX#B_f>{&a<}423esNPN3*(Z0BxrAOM8A^GYrRTcR09J%pwN}rV0Le*5(}er*M_xN#|(`9mC;A38n?EHg`(_b_*vV*za>YP@XQwL>qN|gHo(rwVYv12xC$Fj6+V*w39pb6ugU&JkPQwr<ny&I}-C;C=7K<IKoX<`%G8Q?(izU53t(rTq#A7F2FC~G#M%?@1oMHjjt(hL;SHvz}9_9=*@(Q95jw_${0=ZcujminN${a$C{)v-+!IMDzgb>BJ4BiWVTA<OG0iwgRE3OghPd^vdI9+il7O_%Fa4_tRcE(qlvtD{##MPz-z>r_!@d^^;90;5s@P+T1*oEl7>3O#=Gi5(9bXE*D{R@yW4@SuRnwe01Q6tBdBaIwN(6KDa_lNfy|Y3l|)l|ifrtJmPx&>qpunhsX;Q+%j@d%Ql}ZQ3~%R0dwU=-b+P?D{h}F0#22-c7xfyu?ghZ)MJc6Dg7J+U%}cgDHp&j?$p|_TF_W<a7AK{NIK8oFQ)Z7tp7a8DY!=;Ik#uHpo$z)rSy}XamU8Rk1gAxd3&>PQ2p+s&Oxeg9YdIea1LgD76Z?dz5zY|Xq&q%>qka`<^h=N5W`g48mZ`})v7m{z*`R$nEPgAkoLfxnh<j`S0`wr$g^XrrwpaisB}6*&f5AjkBly5Uv4v2QfXPrX>M(S64UXEz5CKcQsbAke{qX6{$N5#4vp8uH<r@LL(w<2(sbx)Jika~|h;9|Wayp$0K*gXmKFlvlxjV+?C+*P;Mf}@(A30kT%+!>(a7Nj}ez1pjl4`0*9FPq7Fx2KDO@yW4VIQp$G_~EJzKJNG43Qkc&Q!IoG;vvr9qJgpN)+#}W>|Iw58Qh??oNB7LXQOHbx{n%PalbXtB@&J?IPP2Jj$b<l1NFd6l^NXC(;S19ZRjIyfsJTaEFLemd^5E(}E5UQC1o@oO+_<e7+u2wQE<0m3c4YgFa3l<!Q7cH}EY^Nms$6b0z5F7176$EV>`tG*Z;iC!o{1eIeF1s9u?Etyt}_&--@D9<YPB9!nlb$vMoSE6Za>jN-eBsN>$fBS1ndrzbXc%(m4P6fPoMP{t{&Qjv=n1|b`AUC@ZQQW-Y5(vktSsW6}(UXJV}!I}|{(_X7$kH9v^F7D5U{4kZ_G(|RxXy83W^v>Wn!56^UO|*WVqY>Ru(<gAa-3&!^z~YHctzhK)bOdoq)#hbN#$p4t5R@kH*P3@-4x?H|xM`OWMu5g_Yen^K4K#aJGeUb4@w}%SVK*xWv#y^mc8hCjIrx4pfWVT+ledK>^Md%0V=DJ&|MgaOA5EwpVV{_Q6mV{N#br?hjI|B$`ykp-ei|@N=(zS+U}^c%LphG+iQUW-umZ2ozvJl)wZ^~nO0S@R#E5;QBLcv!*C)cvP#aYDCQv~J1NFUzmD4qY&7o_nTonK+*E4NX(1Ls6?{bj<uje8y`gv%wnDDrxXMYOVsJM97n=0X8;B7OiIcUJKh(7x?F|tv4Z6Sj3Vp{@G?-ssRA{F<7gpyoljCrL*$MB~@u3^1zI}>{)m`Y#gx@i>0Tiuv1MCwlw|M8PNV=tkr`_HXTjLXH^f|a?R3VbDJYPKQVq#qLH3qp21F2dtjS4P_HzErVe2CJjYB+`=toTVy+tu&)oU!h&|5`;_YF_d1oE)i*zw~cAK+tr+{4z<SH>ov(^#2w&8&<hgyN-_qGU{YVF-xi*Sl(tIkXURxJ^F9#KyYWv}@Ks5R-nY?DF5oJ`8&kxb<Itm}5vH^VFaH!}J87}Y&a5&hTA;1aEen7|$Qt)s34Rjgf0U}lIf%)=Fu|sFD5L`Z#3Bs2^8wwDHj!A0>noE&l{J-K_dL;RDoUdPu_D*?<yVnX5KBuN5h~i41D&Ea7hoq`tp?jJT=fIDa_5Dqm2%*O^7u^N1bCh5u*mtQDP3f8WI;FuN;D@@dgEg>^-6Th?N?sm6$S<q>n%v4opoUF!v?M%-&2Rml$9KCo&v;?ZKCVqRQJ*q?7FpZZjvP26Q3mFNZE@n^#_i#$<(v4!hF3@?ywafzOhJD+ML8Hc(c1`&frc((`B`9BI8~aULRF?qJ$@20#{JqsS7?Coa{N>1Y??0qvEiTRlT_et`z;Zyj395DJDl~t`~h3id2(2NaZ$s8K`U1SjfI&{RVi~tCyq^nxH5YN~YRMY2+IboMx}6FbYCBv?CLw3pAq{pwn-lxI;$ClX*?RctIOu7SWb!JS3ttynX>86+OTJSr&OD-B`JnSgT#5OT|C{2qE?Wux7%&0OL8`29+DLz}3BId>-?JPz^M0X5yI+Vrwae+_yP&%o1H)bEF*XRQcE2qM7(U@xZ9@>^PunXtoViBHh_;nUF=Mscj~`E%QBSWoGcwR8^>~a|4Vc{GH6`^hKfy7(5;@fgL<Nv{(cA&}17?`mo#Ub^R||MXjsxA08u8_pG=Xe?(I@t9LJGAfANN<4~!+;WSdh<_Y84TM3<{%x{fyZRdhl0sZ^d4F`RQg%<}R9X^YPjmU*<)GO8YwGfo+)dXHL4`ra9D8Smps=ejk6r|1k%xn`%q1>GUP&dYtvONct#8Ii{PVioCh6W<3)N$wpG<*Q;EZpj={&>&4(z^xG+XCFe{ijwh?rDgG+Fj5qQ!m}fPABL_eB1;~%<n}f<Xqr^&7?#-@M=$U#M0*hk@G&E4^oM6pmEBxNkXnH8nHW6fXskO4AVN=R!v!2x#V7+*+vi|)H>W^=P?afq$)?Rof*GyJeZW~s@tu0nE-HYjn&1RcvczQCs1l$I60~m?LM40hIO>QyJ%dy^BpVpL^;C*9x3+)8EZ>cMO#s8IalP*tmPNzZOaL(z$>M~eYc>T^^T}%Vl$cy!bupaRlNb26?o1WDd*NwSw$f->M&3fuu~mi!O^Vq`p`~M-!?;Cc(Xp<la$I$opC5z3v5WV|JyL8;IVFX*1NYf#Az#Z6MMZM#Fv;47x`7<8s3$8A*Xd&p+~uG#PU2_jpZ6Jna<JPGY%n?gnuaUprr^>-hA3<nr^?ziIQ5O<wU84o05XHgJxf2%K{`=)q^j1qL!jSN~CmjL$#wOy4}KL3GWE$6~$0TnTRb(G@0|bZ)JouT4Z%wcibUdpbk)a>>KaveeO_Hv-tI#wll@JfHk7xfv6#{P5JrL1Z0@(i)egJ6Be?Klw(lZv#$scN({;9vNq5xvOz%dk0;aYN;=e|fiYn@Q~m+3Tiv_oSFvQy>Jh1<epK2QDY`Sd`LV-?nuDjJlg836yjp3ZKxyQV)elf@k~ig~8!tBilQIM!C#@il6RPMRSiHgSadWH=mcdIBD3j~V$Vs{hNfZOnA~rRlXU^iR<lT4@-sV7c)cNCnwn>h*dVxAdv)6KFJV_+U#=m8hX~^B_u9!71<lA6Nm%88EzMi>EKtUu@E7sqa^{|}$_+rklFvP@b5zJ0?p@&G7z417y$j$DuR*0!9Qd#lzs#OLQlG`|#D6$_bJ^8#Y!TAO5m$4!8LQ;(~<)W}j2nDM_w_G8!R=S)0mVEfi$`wjs&@h10L~ovkT(B0EI^G%|el*1wvPf5|G3@!S6i7uQhx|}s4cTpF3RTZ`=XD-eI`1VW3b1Rb&dH3@qv|)>Bv!Al53dI#@!bU7DfywkaR`A#+Vx#EY|Q#N#UYwq>OHCh9WyT%vjjFou{1|K`(}VDJNV1yUA;_MiiFQ<#n^>XC)XD8(7bL7u4o$HfI4@o6#7NjQAkkhR$f6EgzAZ}Q8LLHTg6A;I|W0r6bj_6fXM)-NR>U#P>jCYjKF8&R@}2{uhJ}va!T<fNR>#mDP?U+HOEs^>ptt+%i~Ixpz^MAl+vgDN-5^IDGGQ`fn;uJ{n{liW(bYVmXDzHAh@FG{EF3@V0K6BCZL7sFZ=>CE`4VZq7Y_9UmvTG0{4Py>q16t15d^AN{3iM-LmgoDf+KR41WEuBN5@aIu34TOJw@NNzDb;?v;Jo3J<QYV61>y+I)^;KNHkwcQr9zL9{6rQFT3T7LuhMLQLSl#w^zimW%Afkq4aDUBtkwPj#n)MQkjBI7Kg&yC!d%x{!3eDorFSW0Thd8ed{&sR9G-C31(#;k9qhD)51sfnbjz3mpPkZ_qKeiI_zUSsk%~%M4u}sZuW^&LIvMOePML+PMy`Q$NlK;~0&N4om(}&X#VIS={T6Gi(-YGZ1qklQ@Qv-=UQ69j`Z`2E~NkqSbKxPS0Poe!K053#b>Y%D0he?FZ*{dJP4Uoza0=<&@8%{C5JOIJPQ+hwA752V^!}%m')))
_PLAN_IMPL=make_agent({0:_SCHEDULE},**{'hand_align': True, 'weed_repair': True, 'sell_lead': False, 'budget_guard': False, 'room_guard': False, 'clamp_sells': False, 'dead_stock': False, 'terminal_liquidation': True, 'front_run': False})
def standalone_plan_agent(observation,configuration=None):
    return _PLAN_IMPL(observation,configuration)
standalone_plan_agent.telemetry=_PLAN_IMPL.chassis.diagnostics
agent=standalone_plan_agent
kaggle_submission_agent=standalone_plan_agent
