import sublime, sublime_plugin, re

class NumberPreviewCommand(sublime_plugin.EventListener):
  def on_new(self, view):
    self.run(view)

  def on_selection_modified(self, view):
    self.run(view)

  def on_activated(self, view):
    self.run(view)

  def run(self, view):
    statusline = []
    for region in view.sel():

      if region.begin() == region.end():
        word = view.word(region)
      else:
        word = region

      if not word.empty():

        keyword = view.substr(word)

        isHex = re.findall(r'0x[0-9a-fA-F]+', keyword)
        isFloat = re.findall(r'[0-9]+\.[0-9]+', keyword)
        isNumber = re.findall(r'[0-9]+', keyword)

        if isHex:
          UnsignedNumber = int(isHex[0], 16)
          Number = UnsignedNumber
          if Number >= 2**23:
            Number -= 2**24
          binarise = '{:032b}'.format(UnsignedNumber)
          if UnsignedNumber <= 0xFF:
            statusline.append('{} -> {:+d} ({:d}) b{}:{}'.format(isHex[0], Number, UnsignedNumber, binarise[24:28], binarise[28:32]))
          elif UnsignedNumber <= 0xFFFF:
            statusline.append('{} -> {:+d} ({:d}) b{}:{}-{}:{}'.format(isHex[0], Number, UnsignedNumber, binarise[16:20], binarise[20:24], binarise[24:28], binarise[28:32]))
          elif UnsignedNumber <= 0xFFFFFF:
            statusline.append('{} -> {:+d} ({:d}) b{}:{}-{}:{}-{}:{}'.format(isHex[0], Number, UnsignedNumber, binarise[8:12], binarise[12:16], binarise[16:20], binarise[20:24], binarise[24:28], binarise[28:32]))
          elif UnsignedNumber <= 0xFFFFFFFF:
            statusline.append('{} -> {:+d} ({:d}) b{}:{}-{}:{}-{}:{}-{}:{}'.format(isHex[0], Number, UnsignedNumber, binarise[0:4], binarise[4:8], binarise[8:12], binarise[12:16], binarise[16:20], binarise[20:24], binarise[24:28], binarise[28:32]))
          else:
            statusline.append('{} -> {:+d} ({:d}) b{}'.format(isHex[0], Number, UnsignedNumber, binarise))

        elif isNumber and not isFloat:
          UnsignedNumber = int(isNumber[0], 10)
          Number = UnsignedNumber
          if Number >= 2**23:
            Number -= 2**24
          binarise = '{:032b}'.format(UnsignedNumber)
          if UnsignedNumber <= 0xFF:
            statusline.append('{} -> 0x{:02X} b{}:{}'.format(isNumber[0], UnsignedNumber, binarise[24:28], binarise[28:32]))
          elif UnsignedNumber <= 0xFFFF:
            statusline.append('{} -> 0x{:04X} b{}:{}-{}:{}'.format(isNumber[0], UnsignedNumber, binarise[16:20], binarise[20:24], binarise[24:28], binarise[28:32]))
          elif UnsignedNumber <= 0xFFFFFF:
            statusline.append('{} -> 0x{:06X} b{}:{}-{}:{}-{}:{}'.format(isNumber[0], UnsignedNumber, binarise[8:12], binarise[12:16], binarise[16:20], binarise[20:24], binarise[24:28], binarise[28:32]))
          elif UnsignedNumber <= 0xFFFFFFFF:
            statusline.append('{} -> 0x{:08X} b{}:{}-{}:{}-{}:{}-{}:{}'.format(isNumber[0], UnsignedNumber, binarise[0:4], binarise[4:8], binarise[8:12], binarise[12:16], binarise[16:20], binarise[20:24], binarise[24:28], binarise[28:32]))
          else:
            statusline.append('{} -> 0x{:X} b{}'.format(isNumber[0], UnsignedNumber, binarise))

    view.erase_status('Numcode')
    view.set_status('Numcode', '{}'.format(", ".join(statusline)))
