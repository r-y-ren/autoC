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

# Public demonstration plus local stock/budget/weed guards; a proxy only.
import base64,json,zlib
_DEMO=json.loads(zlib.decompress(base64.b85decode('c-rk<+m0Mpa{QNho(E0$a7g-Xmg*IWr8ELB+gJ;PAi!%FFxC&U-wgk|xifvKs*H??%sNd<_5uRb=xJ7+`^k)qjQr`pum1IyU;p;kU$6e@r>h_D-@m{5bba-2zx>C){O9K{K7ah%FTei#U;pd#=bx_r@bND{-~aID`}?<7*H^C|_E*<8pRS+2{_)+zw;x}9`279;_3r-j|DS#O^gq|LN56UXr;k5Q{$cWx_q(@m&yRV0!Rt5gc30v9Y1`@R_pf)m&n?(4oA!r~Z{B|U^XI;Q`1ts=Q_Ci;KK$Fqhw?AaFOR?DU0sgY+xu6$!vklH+V9?fc<l7)!w(PdKD?fMC5IHw*-biUhaYTb%~-y4){e!P#)YKc{>R<!+j+;A6E%I|`O|USo<@DtSRDE|T^sZFT%-0KHq=j7ukP_My#ISAudlw}y?yxM>U!h1Cyvh3E3Q$)7At1j4B5^14<DD)9Q%ou9qOL!#B#~q;JJO;6Q{qB4jo1%8K)mUoLaYd(c{FG25Pb&?mz6_@mG|GYWbweiw~oSTcF-|80YZ5;}g)i6MGf@^z>M7^UYflZ;r*K<c{>=Z>r}v`hBFo<$*R{7oKSkaPM`=qv1DbQ2hZ6&zXOUhloCf&;R^<P|ePZbhNS^c5LJ&hluSiG&J!z3XeQ?A0FN06FK89@W@vWZ{O}-efas0yLTVnynXY}^HG?u=G@$y{kM3-x9=W)Oh%TONsFf(e+o~X(+xtbtw{$LRxG^V!}-exDzu?=$%A<Xohyu19P`+`(>JJR<k?G$U^9OY8m9E?-Tk34PanLA^X3aInDf3ky?1($JQ_0dw<)W@umZtLPey1QN`C}ILqPX&7q8hLjtxaOLEP!UdOY<se0ch??C%Emw_uo~kw8XmY@*j|^!!q{JC<ek24*0~D~_}iU2xaV^}ky#a%RI<`o4S)v@u(wkUZr&^rm)%XA8=5lYq?@=O`LKs+rDXnUzzpmD2}z4V=?+hM7#QCyue0m@(Bipzv4HT!=n7*lf{ouu!hWg<5bWC939hExzGw_uLcEDts~!v(2XwrcxYd=$pyC#E>Ipj-_Ki1~*i%&ql@@2ji9kMp^7TUjl~l1I(%ox3{uCKm?-Ib8h+o--V$8Xpi4647T?l-rev2uzUCJFBXW)4xVLO3`~i?J=y{%1B=-)KE^~}|N8#jpL6>uHsJhwey92^I2sU>9|>cQd~h}i7;$9Qg%1<VyM=ebp^G1;KRbP1Yow)S+icYF*Hu{0czf;WY`()bn|sfX(>Z>UY`<#gBDfp|cnzT00?M-;9UxwO@EuEF1u9EQ2Vo=JN5WKbnP>NQB@VnDb#XGodA-R_1}2#XaKaa$%xG7g|FJR{O>=(n#=}#!y_!z@xn0qO*Y9T-BG{JHY=`E70V~qQXAjUBu1XEtXxlj#F9ml!r&wOMtB1*iU^laoqEV++#vVau!48F{P-gKOxGlFsM_!@pT!QE@bsLZ^<)2o)6Zk-1$Z#wS_h?HMm@9+cL4m)@JHS!nf$IJ%kRdnLUPZC{&KrbVIoAGWaSaOft^)U6o11#B!sfm;ZSKwQ!{+u4Nqk+eH?cPrGur($&X7h=A8OeWj^cUi$1pXsCaWxo#FCy|GAa~Zu%x4*3JwGVajZ|Sjd?E!scy7zjj^uJ_F|+VnKTOuH$Wr}R+NYbR-6;g^0q-O*oe**7_Q6{HYTuV8(8q{8skG!8omS=_mAiQ|9Jj>D58(7yf0%*{sveIZU|i84d}!i6#S?8GSs>q$8m_qcE%934a@>0o6|nmk#A4Ow(<jjon<76^vuYU=_>8#ig^<!Fp>t&F9iOj?k{4Gtsn^?q+kVsL+@c=C7j&|7yC6Z#SVP{_%jP%XT*ygGiJ#;xu8XB813sKyG8`D^@4&uycSiw2wAdb3^;E9wDI|$#`oYK_T<;)HxxF3#XANbe}xMWuK!CA0DK$swnn7Fj5qWpvC9fnf*T_d%rpF0NWYN+1j2aNFj@8dY5Gt0P6%-S@bLM6cZvvmgUu<B^d#*!)8;D?WlzskRxS!U9|qnuGmZmxSnO}_fB5!Fdl090gdFpAoYI)s&GMme7ZTM6fK|TGkT_6r$bi)2FXITLe*tS}avS1*)>}xE6SzE4pp~_GinCJAZj1^8fRh50HYQ)GV0mfeJu^LG-%Gs$J?Lk04Lfpr(~xA`8yG$tbE7Y;ch>07`tsew!}}c)csVp~jXRmm50f5=c~PBw&+H02_m=Jtyai^956E@|`Gj=4^fyVe=2j8FmR*YrEd2$#hm7rXk#2yUUEDlgB<X_9EU?S*Jb@m#Eqz+huO33a+G%{)wnf89bSk`T(#K`=v}MH+Gr1B91BfgKHkQ^_qB8|=Ox3t`P2#2^nYXMDg-l?e{(<jbLZ`>PO4=G<hbm7f_Er$WUsP{=fCD+7U;$a_0yS)_5`nrDgiy9TKy;)KRM_EMLb}ea+*|o-4YD@^S=k=g)^zD)o~!b$bITU=Zng6-vt%_V%^<7M2v#jHAYB-vIp`W&EN9=c)QBBj^esPl8JMU+82u<yq-^T66p3l639I*k1fhM53krG>v6Pjkibs$H6Ay{fC~>B%NC)EK=QqWW`<ioNx#*4f?Y5M4t8;YV(7`i#J0J6NQj3g6dN!vQT;AdoESR5cFGk{ooktK2RQxL$v85?pbsYkk6g!A`$j;kl858IQs?#aJai}E~*`Q;#(X+W4(>0vT&<$eMX&jr(47K;{ME^$bNo3iGZ<ls+>75<rAm^1t4tOwUFu)ca8g1|0=DC^E3|efZn%CIQkO7h2uj)vC|K{zV9z$Q;g@hExG4ABC$ETL4==qKG-fmmAu3^B(4plgT!01u~hXdKz6eMjM$NX#rmKoMt$%O$V(Zo9m_AAoOq=?}9JRu;1ldY;#ES$=2TRKLQO=QHeXcBrf`#_{_dQ9a~0aEp;xfmmfAX;oP{S1w8+e>90pKOVvx-LxY;v#Kfgt?MeaYKV!Ska>E(Qnk;%7smpjg8muNITXnJu4`^QOcGR=f&SA-cs!9Cq@g8-Wx0|VqSZjO8f}<71=7_Hf14wAvOr=fyJRiM(T_bM->XJ8N|$gDC>G{sjI>s!RD>3g}|Iu#5~m{2g=QJ<cCRk?c5Z!)K*d5smDWeG<)e@?G`Zfw4_~NoJ8LH$IJYd9nsz#cr@t{F&W8~78a{Xl+G>Ht@fXQ<sN=d(+~B`Vj{El;NXwUE*k0YPdwNy-UMx;cXSzva{j3agiRcc>@#C|hu?)ojZ_y<iLF^XZ%qK#cNQa<%#d&tsbE3r`t_;#2Fm@HdMlaTHtoBJ@zg*Uz-gwSHsHg%q9)E7Pg$rd7gd3Is?_g56mr^F3a?~!>XzN!nB7M9CTi5uRg8-YbK52HR&Oj8>gmq5-iiG7m%9&Ikl+(Kyq)$N?BfIP(kqIE-1)_0u+QUdQbu-7sJb5>zQ6zQP^$EJ<aM&4hQ8+cA09{M@OI^?G^dZ~u;Y^eoUNSSfba!T<5JFpE%LyNY#6JtMwH=<6n@Q=r!M0(*Cv6E!({CdysbZvJ}Y{00s!xfRtTUV-RN!*&4jqUy`#|N6498%X6Qu80*L&!VN80k`e+)QU!yFsMK=C{0vJpDeokCMx-^%Ix_mTv*qu|Ml2o{`&Y2NS=j+EP=9!#mu_Nv!YIE>ehBcP}HFpoQ$2$d^L7XtxjcEf?E?Z){ckeEqzW;)gDYjG`>NX`Jz%Nq_>ekQhcPe&G{u@%tJ>oA6NZMO)49I~LM|-=zB12yy#$-Zc9%<yKwi2iB#Z$P0-#N9mN2tyNUy`oiOA=~4n9=qj!E-4kW`s`hS2$J&+#;{6=eeN)1DU=_Md7EvrKi5q-T&mv`>MrFl3QJGtHfQl*+^iWtMrN!;CTMG0E2Yxz#}#2P-pkihy^S|3Qk3O`7<jt6S04$Jhwc~pCwsT)7H^wwgO^Lgu-hNll(k`?;bi>Y~&@Kei_WE>G!8S6(by6xsUKM4h!MV1GUmF^Ar+w5Q6m_31`!J237!gn7RD%T2GwU!wA^5ieNkrz$xJ5WP4&Z7#ZCF#>;>&3JyJB(aZUC)?kapf!E+&t1c!0>+(wX3;ZYrl=I7_6Jtx)Sp*?ZzcQvL_B_PVW<b;88*mNf?HO>?<oG!QQ(y#x#8aaefu6O*5nX;yws6-(3R0>MSQB7{+KWTv8U_;PBzR$H%6VZfdREar5G@QMB0G2ErZ+An5B4%E!Hva?LIkKVx+54BzBzl-P+W-80swSziZfNXT!2>REh2yWxP>ZHw7yml$W2dj<GEkF($6fOdV6t<?ygbk;xf=2&wrlfZQLZTSv9#U`liwGr>dEjK?=!poQ!rhwJY+Y1Qm$=0vAG|0+FB9#G%JAYVftMX9!MI%~yjE|H<+qYO<{2Vp3;ob|Wi$SLK6A$S<xmwIG18!I4x5R;pQ&F&k1qfhxR42peO2Q@<g#0&HT`)GbKNL>*ym?y33ON|g^b$)Q5~PtG8uK(i`hNb4sPDG$xpr2bSmVD#BQN)5>HH%aaRi*r7=yr(tuD}n6@#()r!`9F@?i?Dj-2tQlSNQ)ilWT_?x&;sQgr((k+&Y|Kg+QyVklgAC{wQ}w)+6Ja`B0gb%77fTH+(Uq=@jDNVDOzRA1G}|wFf6m_!!ivryGu{uj+=Xt^tK9Ef2UPCokglUPHzzJJUhEXM&FX{W$vmjy)mmV-YI)tjlF>Vr{Z948L6ezL=G;Yvr`sY@9F(8H5!Al&wgDc9ZrGaad8ZWdg7Ta-xMs|l=92T?liKd<G4?kkyW#s@NiANp;NPW-+h-rESFWBwLv$(NU@iwd9Vs!Ou9Tp;chRbEd-eWOur__*rb4|0ll%YxdqE%n~c}9&RBr86zzVS7(zWGRaRu`*;0Olti!`)0tw^Khu46aSO9&Tl+9rb$0{4o@KKpD4ZzCEY%+x!Pqn1rD<X8!PHrjC*=lT4Wv#iTl6oZus6<e#da7DQkU1~X&8R}t{oS(Mnwx}V0^>Y6i0Ls}oNPJa3uG^r>n34yUZTM3^i^?p;D(qEVVslb-<J*`AljAtWCC=ec3M)EU^0tkXT>M}`M7Ha;27-ZHNL0b5<2eWf`inv25XLC4<pd47@AW4H2%Bot3jZpungP4RZ^^IvCD82$f1A~cj~a7Qh>{I?aiH(4o{gnw2~|aB=NmO1AtP(4aSBo;tmumFeNSWyTJ@G&?5%87s;IWxL<6y(QE{o17aMzU{d1Dj!3a|;a)bZV^&xNvk^jC#BgTBurxSX0nI?Wp}G$=aOvuz8gXfYW{#Wzs3i0zLIoTU10)4gT8{jcMij==*uIcpHxc0I(bu>bwt1@^IzM%I?=ncu<?=aBG$HDc58Y}uiacQ{ux+eeW?YHUOCmrbyw?kaIG^3~H7IYs0zJ0f6sA&Oz>(6)f>Nc@K6CDkRdA%cj{s<kNifI|nP!~i;d>u2=~3Te%b`99^F?_wbO7H_RJ-D+6te+n2ECb;Tq8pHsm?~GV=!aDzXqG9zRUrCBOvU?xj-9=jb91yH?X}r5{%CCjKAPve{tCA(3t~-d*OMc*5XR%AW(2P4Cn{Ggd<J^$HY5JdsG2b5Jh~tw>c+)yWDfYI=f#a)y}W6!hMOnIi~iut^hp(x6Bxouv~nJ`C^c8zXI(J(*G2oK%>g}M4Q?42hE=@qX))h(24>X^Ewvh7*H&C101j+HUoD%JjMWYvQrh)hobw1pc}VpSs@B+ybp`Q(42chNatccb<(MTf>O?N?heSbA9~TjVP6!IU_F@9q#j-IsZdJF#KeO1<s?jAW`&llV29JO+0U1KbNV68?3W2q>h4k)7}Hsk_0fbZ2i;Aw;?@?dmF=KxPEJD#h5QhFfuqGf$xP@0pucJ`_D+Klj2VOP%gn3s3+?q0uX^n-on;zlm(;0%wggQ<!)4<%HBR|EBI6@ZqunN|M=Ya_q@t-M=T*Q9swtCAFD-Cm6`Cpd=*;nQCF9NlS&L`Gj?z0Dsx#9eh^eOuf)JPH{4Bj~$CS?mTwB!$pghbz;n}3r!gY7#O+(-ysT0}_i}(c%)vFvE=2qG;UQh_itKkb06gv&jvWrjV(s3lf<HL{y{G+m;NR6!Nsx%`$aKN#aL3H<9H7W~`rJ29OTxctaT$v{hB@jdkRwsH|x(*o7<IEj47Af{S0t+BXw+KbfIrgO_jMa4v2|<~Y^*tcnp^McMoG0fe1=gAZgH&T#BE=L<1qW*#HKBw%J*cb-DVShaz!{q6xkz<)1WVyG!MgRy&brZTR4Mu$ptT9^iKT>~J5Z@H4v()KF>^sAMOUtJt4^lPc4?x$h-Ui>6DX9GYYDxON(Sg4Q%b~M^!KiU)JQZfOVfPu^%!MahN!swF)mJBt_%A9^=|j0<>H=B?vuY4eb2ta)(}qE{L4evZU{Z>g+an34u$#tu0T95f3SS{jYq6%>pU%ePoFFX6Bxy7DrHRwSBz;$snZ(g2St}vH?XdQ1|2qvsdvHA0(FM$goWVqv>2vPDa!VQun#4TtzK>7h(<o`+XSR@g`3iXxjkhs!of?tg6y6F*@0pSmRhWysyHvqlTCW6-n3YfMWr%vwz*6R=EuYJzgUe;!U0&p+}+~EJzB>zjOohb%I6cAIT3}82y^3SOD<k3*r}qD;=Vd^jM9}64-r`}P)OurPu(a_v}%|txOB|W`N(-elz#%VH!4IXOIeQy!NNERJYA4C?U~7E;Qe~wR8jJ>1N?|(+LU>-ST|NBY#|8CqF*gw!&$xRhDxG51hF1-D&+>BM#m{sYnmFhfRl%S6{RvQ3kU6iMY^94Fl9pTQhh2LRQD4&aMS%Wpthxh5#9XO7*~0QVWq;ONw~6vyJjL#7w2JZD?BV#5c49;tL-J2R~5``7452=FgcorwblLNOsvKXwFp-_n^*UZaR%0KlxhMV78R>Q^LF5@0^CsFXmG4)eO9HzOL%vd_-@e2EKpaPoFeXvYMMke%kwlt#sPoka>{J5ZeLHn_KZY%@Dd*>*A*6q6Ev^IrRML-D2%BhaVe3Q(-9~s!kh?;4zMy~2w${#ytN#4ZUdXKjT!(2<??cpTE6Mcn7?~5AwJ<uqG5RoHmla{JSv+7UxD+aBdB<BMJnifF-aOf5{DdrLUVVqueCGp74LLqp*5eQL8}?Tn&S#eDs>SNH}ev#3f!|y6IK~kp(+#X8<apTiFn!>*_n_|AM*n+g-z7tRaB^&zz~F)K*r3u!TmGvo(kGfyBMr0O<7y*EK{BYNlTzV;vrV5<F{|VvqFuOORAJ8ti<*Cna@q!o8{Eq^(5GQHX^qX*JNs!)yig~C^s2+xcSPOWj%&j2{c3y;R+~lDA|lJ|JC#|DLM9H1%Yg%vz<WpKTGJgFPFhIF@VwL`EARb%#uyu>C#nH3>`jMq!l<vEoMB1XF7o9^=d`3cGXYA*Y%>ZE&P}rNc|+nXh17FNK`1bl*NY-*dj`<F3RvTiulRY59p?XZJ9A~aMe$Af;e0rbRn%2HB<3do-{)B{hN&G8Yj<Ve%5M{6iT6a)F@UmXK5-cvzOY;<~Au1V?)LpFV5;|yF;K0<kmrZhwWZ_gIupKUMYPtTGOnQu*)Q!Rrh=9-F5i^i>0KLc{*f36L75hZj@03iDyq+*)t1=7gZH{T0$!*Ox&?AY)UIJj1BgtdW#cKr*eXL5kH4qu}Fy<J7sH%PB337!?U`n#WtnQg`;HZo(f4_s!{=y?zh$Ktc1{Z$~0ZrZ3#^wNVe0F;us(Sl{B|KEk55};n9=h@pgK};}-?$kW0y%p=X(A`#V=bTMe%Pp5B+?-fddkJ3lY2&%Qej(>Gz5HlJ2IMbKMQ#lw`((-uRcjKUGp{}qN-HG8!{d;q|Vn}9`G<F>Yz#WSGp#QH?Ugcy`XT&ewPZoi>;0&xGlteV_FT}1^Nw|M}rAd58F_;s&3!%C8vZA+6(XeWIlVhsuS-q<e+18S$VHRRQbKy(6~!d%1H<_4pa9u_P&X=wE}lhr~jaA!(63e@UC;_q@1FI<##Sr^6!cr5tNDUGI1tmq49W2hwRVH_MCNHU}F96C`2=xADTe5gf~<Fpsd8+7mzcCfJ$NhL}gtp&*iYI^8{K*bfAmxcq1F8q9twc$CUEMKZ=;?jOj1{fF@M=`ax;~Ze+Nc1@DqlwM9#2=V9zDcV9r<|ssN*_`H*Oo^BZeM<x^HdGA#F3SE|86%#4v|-0=4T^l7hHa6xPx4G+sfXebwA9g{c#n>3;XFw6q$&H0;X8SF${y~g891a<~hV74pJ&Mfi7|_t0J0(Y2rv|z!{0MTwG-BeM#K0p%-V-#kP2B@oRapB4^7q+L_hjtT<!wwnGE7tB|&B(z?*xSvl@<q(D-WbZ;jQb6Vi#wd1;FM^{&r&5GDoNllUQ6U8#*NtzKLFh2-f=nJlSK}Af>PrkOs(fBB<s#dr$uU)~@0!+qi7cm`|G7t0K{q!K1z6-;`{u)A}RTYGaiUM~Cew)4!k(P+@(2){fxxsFgnoA~LVAnq7%gRvnDnUkFrUlz)H8jzpmZ)OPJW6!AiVs;_s7}GKG^^Ke3Rmn^v;Ki~Veyorio(Hd=DMw|KT0z7(zWa7>Mbt%izhNmLB;)&A1DPL-P(oR<{Y6sm<@MM7<5je6CP$L0TPgF%zhM{Hg<l(YS+$om1@CFtSgYoU1`+4uMI(^%yfEEAyNJ~UOGm_Sm%^GK@TNW1!$1`gTAjJsO;9C6{O`A_gy8n0S5Yb3gmUA)Vc%v&<VRePS|sByWI%@Gn3J;Qp<Ueju%GAM~0(bZmQ5Kr12$&LB9;dDAC01Z0pu@jS2A~pu0X>m=P9F$RYTVVJFxb#GJ-xVud-Qar>#ul&d8hZzXjGF@elP7@CATtXQgFWFjm4rqd)0(AkF?ZH67eNiIn5k`UxgKN%U6gcPf|Nb9n)l^bH2(>>IJDhQP9D`MD&kj5;<rm88Nl_(4-A9*L`oJn7(kp<$I7*ORKrmX(fNopVByD|1_A!1ajt&k4tnyjSS5|tcjphe}MJw>!A<GO}Z!N-|d9T9_(4}r^ukS?J}7H~-ka_wYpSd*?hBn28AIFZg|Rx#kmd{@pT;b-wPj+X|N8{De>blEgtNC?YM2|u!C78x19IJP61qDA5q$<W2_#e`hzF3?D_bR1<n2KN-@Q9T|Z!V{`xQwT~~P~NB@l`;m}ukzu5m3~|`Amc0#*(~zWJ7_eX?}4uS0?JZQyxbVU3$nKgr=1&&S*Vi|sQ3=-otFZ7r0hVMAfDY^2w^-<JW6YmQ8>wzd<oAIHJ3i2@4~1fKEs`gCLZB&-&4DZl+)EnB(VD;(`;mwTqiffgCD0~PWMd#n9P+;pLz_Hv^<g{;<$TOsfRf}88Ejg=D1ae|E7sJjwqnfP(<{|MFm?lqF1(;D$42>ixsR^uX2Rz#4vmMKjfxu(OyL@_3JiNsaQxc&AT9?Ol=B#8xPg%(&Wt0QSLSXAlE7fyc*7fbkTx{nzUV%A|g9yI@l#;(i#e^wmOb~?5?fxBX*ajkLJwt9LykR4;av43Ew=~i`9=QNvdgmh<*km6$&T?0BF8h8N_XvxSJY#_^vIeN6AyP<gku5m%^w7-I5Y^9DSuiAgzL}89?fA1@n#1vmI$=lMZu>vLo3vqvin!#Hy4f;r^`wTxQbXB;7XyyU})lx}N?;4RCEM2lKf(kF2IG$OKWwy?GC?^;pk04_PUb!J?|O;ArqfP#F!kRuInu>I%BcoCk>labWY+7oFH`wF>n#tDFAOJ2rU|{q!_^Y11N?D8f_bwO`YU;@PKC&jb(CmPw&LiljLnmoplSC+O%m$Z~WUa8?3!1zH_LYZN++z7}3eV9de7?I+20ea=$+3*{L)+(xBU*^$e$pys5K@-W_FrIG*@{K~SIFGE(;ju8is))y>k0g2;CjA|Wnm%Xq`jm)(d{Zc7nyg{vC6e#s1`0|M8aQ;|h|J4$nnFEACocwIL?Zdm!%F?{pSYMJd)dV51v22y2c0E$rykJ^WUS#w$CgwYX+veIKU7}}&3B>0!-4UiN`heVSC5g}66DOh6?{znK6f8b2*T*SyLbMp1J9OsjbP`FauuDu>ol8o*gm~}>W)Jg&-4bB5c8gK1a+Ox(rdo?0vZcqMy2}wM*vuBQR?>?rbu+Bl9Twp7qYmCVU6mCSc^G_MB89eOS@tTvkbtVkydt;m((CAIAXIbZJunKmXrfwKf%0#9L3l^<b42Ya=6cd3^yPdL!10b&&7e0Ly9tE0xLqSK6?{MvnMV1GXUi$OEzl&bO4UL+8d&|{);z;YC)^U9U&lYj(Qsv0<^Yw^y>&3>SCoeIs|Rz9$WBK0=sM5j1CeC7jGm(baVq&AxE6g0NcLf^MB-Nxfm~f^qfy+#B0`pQANS<YW0^&Q4xg4zxlCc(x*((_G1AVu_Rshh48n<uV5xN&i-8Sl)U~y-RjY=w=$)Vmj;u)C1nOPQaaI}H%4N;4#9Gl!wyy$7&n`e!v8D$UkH$$ht=_``fTC2f<UF`AJiZk~#|LRqwKOyLjml7D<&${bDvlo$UNkVGJ(ZKEfS7gjsf}Bf9rQ6IaOhaEo{@XB2(GkhqLL~^5;-@7VTXdVf^;vA4OupfW&i4x7SdE@f-S(bXn2DN6^*T5W7QdQWRuk3^D{Ij@|EzB;rZztlHCV<mBF<V1{7%ex@>He;3YHGtk5t?-!`HG1Hfdw;EbSjUfIf(8zzNfiufeEp5Z-A0tqxTja?B-w9ZdFew<B^nuc^HZ(SHg;O(G3n^%?e1Vv^w?iaswaiYgT*g7fRZvE^@HtYPgU#MpGZ3+!*HOb3V$X;6yd!u-mr<LRKF#9~ValFi!9yI+&cLp)jE+F7T)18a~B|>D%O**m>ECVrx7pobVMNBs{C~EepUB#J6kq~i@>E>9YFec9T+StJ$o04p4Wa()!ILGx?3ji1-svt~KdT5P+E4s1QGN3`eG%tUH+_nU;=peNya)lG4q1TL6BS{|Bn)Q`|BzaCUks)jzO;IW*i+_{y$AlP((rymUo!(YdWeHGB8mU*@<@LB2cl~6s6%xiYUx212HI{1d$7^g}>hMLwU+J0a6Voq{-d4?&IFCXWkNsB321bFLe9pG*C_zPfjzO)y&RRjCk*FP=muhcevZd2a1NOLpI$v`|z`zu26ltfNlK`;WwZfuSQo*KxoB@1GE^nH9Y?ir_r|XOUl4WO-I$g8|rNVuiSw4WQ=Ap`<t`cE5=&~wVpxs)SCEOFr&~XV*Uxk>4hSp0`QmuA2NfF^w2_gmERC1#q(Yoi6c3G+K#`QRORU5{xO#E6oF*g-R%ufEEAd~;6c#>8w_@wmBS0qX%a(ioGy9(}z^jih;IEXB{Hb44z!H`tGcqs+b)Q)r#A@)5QB?lR)DN+}atTDdGwrnsdCG5DalCY^1dDG7Wcgk-o>(DI4+Aa}%nTqv9`m+K_^77t8rfpw`&Y3PBNLWwMCBavBH>O8vBE(BU?<J}HlEP(iwGZ=x#37%r;2?&*CuPVQD5jP~A0`!9DrMmM#;#jhs!G&XOXR#Y&Z7iWg)&*Eve5+5$;IPP_1_7qrvk#V)O9C6ZbcFDN)3%b7iDltLGMwhf{dc`?Fm>ZDyJ2zu{-sPY~Gz*F^E6Tx{%|kOgU{i!;-MY^Mfc+$t(Kn6u{k<D>2t<>zunGOKI<<;NnI0JQKb&$DRc(Xvr6+IEuq*4f(x2?HEEbuq##aPend&0?KoSjxXuUdPn1)ME3KHz%O>1L$>mz!X>g<sPkBf&mj&(?GXPu`PFkm-?mI&EELNuAcfmR)N3u7aXX64C=csu4eUC{b9%Pjw!I1;=InxRzU-zOpP*>Krd1_E>0`3<9918fF|{OKxLL0>=qpR+G!BQDYrW6p_b2`q0ZY5MuzBUWH9#Bn2!ORRQ%UG$a|^gz)%++57%m?-OrfhNc^CJYfW^6xm6f3%U6qy9Pe8OcI+aYgUEx6>Ej}S0(sGblL8(-Lp~hQdr*l`|gZW(?cp~%&&!|PpC)10608USX-}^?XqhwVKR26g;EKOa(T0%iY?o~GmVLU%;k(R4g(L8klS|@XT3-<^r=-NG*)0AL?3Bt=WepEdp!F#2u`J8RyaAq%1gIB4txS7_1BV`49hL{0dV9!CvQ%K2(3CU1`s(k>`5N~=2G^a-fyT}XsWTkmjJTgtvET0ca;s~t)ZC5p^)tn-F4TKe*Tu`bU5W{aPC@hhj^;3f?s;J(=*t!{o=nTswj`3QB6{(4OBqe)NT;T;v-ahs`%hZ0R%imCBfd*(!+1a#@u9PNDSMy42Bi`fFQTXhuR@mOwfH<?%_Tn4PQQ3~JrES;dU4i17qa#uw8zr&h2U=xN;y>YNHf)xQSHkYPw<cxVCN`ET+*Hev3;Q@FELI2_BMMhnubbBFt|7|irKTx2%_SN()j(@&*e?nsWcL%KqOqR$HX)pPuJn&}tbD?k?`0O|E`bOC%lKBK>NU13QW_(44J4;!?`5^}*}ky;QUSnZ{Zgeyn_HR~I=N!tvJ@X&Gd_pwXgq9-M6|l@Fv#DssFJkV&pMU<Oh5;nIi3Uw5t1qFSKyEm7#*F94Z@S8NGIA-n@VA*f*dIyXy<~Uf;=VoT-URT%vpu17XS)nxOnO4aSfT`3&lKkx-%(O!RvYR_-gDFHI)m6-jmzYjdBst6W}SCRZQdFfzOlZK=5Q`e87v6!5HE?q9y5FQBzsDEx<sYpi^e%nsz6wd0!1|(ydS>ucZOf%M;o**0I^8m2|3wY>V22P6#q(u?cpnS&TkOaD|u}T?n@hF=Bw9IXZoGb@t)<L|IyeTZsTl0j@pGxa$k(jU7+rnCl!Z!cUGNJ6=h|3L&8>@`>Ut1~XSnFI9LcCdFlUvmyTm{$Uf9^eehn)Hba<Gd<Cy_`EQzYG)KTiriWtRUIcI?FiWMl?orOg|;z#Z6+Qq!~#U^JH4vxO!PWlplc9Q2gFWcGg1wo7qcjZ91rkD_LXwFra|V@H`xkO>zl!Q@~|}cr+1(OmddsXL8+R!!TX@Au3ib(rv-rx3L#3*K{xo_H@6jz1AFb>KoRmxXr-m8SV_V$HS@x3y%{ohWL<nCs(XThN7S#S5Cr6!^Q)Twbuo*AYIWVS<-nBXyxyeoAQj4F!)JkWMsSFShMDmzu3%Yt0<4@{&o@1h^pDVzGWJs(f;`E%b8ntI9HnQ43KK8N<n&!$+Lp8VOimYJ2Oy@_S-w=<AvT{WsC9iAHMb$2vR!wAF1BDbA#8NAr@DaF{H(qvf7sjEsMJSy2wkL1%Vq`bQJomH^f|TFZH%A_`Sux3qCBAR(BtH^@hO`3(-muVMXO4&c)xBerz&#vcLhFK3<5`6Hl>p_fgluRw8?1X(yA>ywXAs_iFRw8ViZ*<M?heHKDY0`mSD*ObU}_!igK0+`JiENHzK=+HLQ^vAStnGrp|U&p=gW~{F({9HM|?vS0*6i*SPfLDI$#^MN_OM+bbn1Q+NS*H1GxWY$k{y?|;x#!li9iaA|eR8)39KPL7T0GjTYPoQJd`zj4-FB-fWcEYMX``<M0)0W@e5=aNl&CQpqdA3&E*AJTrap1l-4G&<QX(XmdSb3pBx>%he9rIn4%K8UI-qC~~lZ{^?dlTZH(fc@qN')))
_PROXY=make_agent({0:_DEMO},budget_guard=False)
def top_style_proxy(observation,configuration=None):
    return _PROXY(observation,configuration)
top_style_proxy.telemetry=_PROXY.chassis.diagnostics
agent=top_style_proxy
