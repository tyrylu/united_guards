import threading
import pygame
import structobject

kbmgr = None
class KeyboardManager(object):
    _pygame_keycodes_map = {getattr(pygame, val):"_".join(val.split("_")[1:]).lower() for val in dir(pygame) if val.startswith("K_")}
    def __init__(self, initial_keymap):
        global kbmgr
        self._commands = {}
        self._current_keymap = initial_keymap
        self._prefix = ""
        kbmgr = self

    def _process_event(self, evt):
        s = self._event_to_string(evt)
        if self._prefix: s = "%s %s"%(self._prefix, s)
        self._process_keymap(s, "*")
        self._process_keymap(s, self._current_keymap)

    def _process_keymap(self, s, keymap):
        if not keymap in self._commands: return # Keymap is not used, but the global one should do the trick.
        for cmd in self._commands[keymap]:
            if s == cmd.keyseq:
                self._prefix = ""
                cmd.func()
            elif cmd.keyseq.startswith(s): #It's a prefix of somethink.
                self._prefix = s

    def _event_to_string(self, evt):
        modifiers = []
        if evt.mod & pygame.KMOD_ALT: modifiers.append("alt")
        if evt.mod & pygame.KMOD_CTRL: modifiers.append("ctrl")
        if evt.mod & pygame.KMOD_META: modifiers.append("meta")
        if evt.mod & pygame.KMOD_SHIFT: modifiers.append("shift")
        mods = "+".join(modifiers)
        kc = evt.key
        if kc in KeyboardManager._pygame_keycodes_map:
            key = KeyboardManager._pygame_keycodes_map[kc]
        if mods: return "%s+%s"%(mods, key)
        else: return key

    def register(self, func, keyseqs, keymap="*"):
        if isinstance(keyseqs, str): keyseqs = [keyseqs]
        if not keymap in self._commands: self._commands[keymap] = []
        for seq in keyseqs:
            if self._already_bound(func, seq, keymap):
                continue
            self._commands[keymap].append(structobject.Structobject(keyseq=seq, func=func))

    def auto_register(self, what):
        mlist = dir(what)
        mlist = [i for i in mlist if i.startswith("key_")]
        for m in mlist:
            parts = m.split("_")
            meth = getattr(what, m)
            key = "+".join(parts[2:])
            self.register(meth, key, parts[1])

    def unregister(self, func):
        for keymap in self._commands.values():
            to_remove = []
            for idx, cmd in enumerate(keymap):
                if cmd.func == func: to_remove.append(idx)
            for idx in to_remove: del keymap[idx]

    def change_keymap(self, new):
        self._current_keymap = new

    def _already_bound(self, func, keyseq, keymap):
        for seqdef in self._commands[keymap]:
            if seqdef.func.__name__ == func.__name__ and seqdef.keyseq == keyseq: return True
        return False

    def run(self, *additional_mainloop_functions):
        """Runs main keyboard capturing loop. Note that it *must* run in the main thread, otherwise bad things happen. So goodbye mouse users. Or welcome hacks?
        The additional main loop functions are called after input processing. Because calling pygame api from other threads causes the universe to break, it's good idea to add those functions there.
        """
        self._funcs = additional_mainloop_functions
        self.running = True
        self._event_processor()

    def _event_processor(self):
        while self.running:
            pygame.time.wait(1)
            for event  in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    self._process_event(event)
            for func in self._funcs: func()

    def stop(self):
        self.running = False