import wx
import wx.lib.scrolledpanel
import fs

DISK = "/home/kwikkill/Desktop/disk.dsk"
FS = fs.open(DISK)


class Frame(wx.Frame):
    def __init__(self, parent, ID, title, up):
        self.up = up
        wx.Frame.__init__(
            self, parent, -1, title, pos=(-1, -1), size=(600, 500)
        )
        self.loc = "/"
        self.draw()

    def draw(self):
        self.panel = wx.Panel(self, -1, size=(600, 500))

        self.panel2 = wx.Panel(
            self.panel, -1, size=(100, 600), pos=(0, 0), style=wx.SIMPLE_BORDER
        )
        self.panel2.SetBackgroundColour("#8b8b8b")

        self.panel3 = wx.Panel(
            self.panel,
            -1,
            size=(500, 70),
            pos=(100, 0),
            style=wx.SIMPLE_BORDER,
        )
        self.panel3.SetBackgroundColour("#8b8b8b")

        self.panel4 = wx.Panel(
            self.panel,
            -1,
            size=(500, 430),
            pos=(100, 70),
            style=wx.SIMPLE_BORDER,
        )
        self.panel4.SetBackgroundColour("#8b8b8b")

        self.vscroll = wx.lib.scrolledpanel.ScrolledPanel(
            self.panel4,
            -1,
            size=(500, 430),
            pos=(0, 0),
            style=wx.SIMPLE_BORDER,
        )
        self.vscroll.SetupScrolling()
        self.vscroll.SetBackgroundColour("#FFFFFF")

        bsizer = wx.BoxSizer(wx.VERTICAL)
        self.vscroll.SetSizer(bsizer)
        if self.loc != "/":
            contain = [[b"..", [None], b"0"]] + fs.ls(self.loc)
        else:
            contain = fs.ls(self.loc)
        nbr = len(contain) // 5 + 1 * int(len(contain) % 5 != 0)
        for x in range(nbr):
            panel = wx.Panel(self.vscroll, -1, size=(485, 100), pos=(0, 0))
            panel.SetBackgroundColour("#FFFFFF")
            if x < len(contain):
                container1 = wx.Panel(panel, -1, size=(90, 90), pos=(5, 5))
                container1.SetBackgroundColour("#8b8b8b")
                if contain[x][2] == b"0":
                    container1.Bind(
                        wx.EVT_LEFT_UP,
                        lambda event: self.cd(event, contain[x][0]),
                    )

                if contain[x][2] == b"0":
                    image = wx.Image("ressource/image/folder.png").Scale(
                        60, 60, wx.IMAGE_QUALITY_HIGH
                    )
                elif contain[x][2] == b"1":
                    image = wx.Image("ressource/image/file.png").Scale(
                        60, 60, wx.IMAGE_QUALITY_HIGH
                    )
                bitmap1 = wx.StaticBitmap(
                    container1,
                    -1,
                    image.ConvertToBitmap(),
                    size=(60, 60),
                    pos=(15, 10),
                )
                if contain[x][2] == b"0":
                    bitmap1.Bind(
                        wx.EVT_LEFT_UP,
                        lambda event: self.cd(event, contain[x][0]),
                    )

                label1 = wx.StaticText(
                    container1,
                    -1,
                    contain[x][0],
                    size=(90, 20),
                    pos=(0, 70),
                    style=wx.ALIGN_CENTRE,
                )
                if contain[x][2] == b"0":
                    label1.Bind(
                        wx.EVT_LEFT_UP,
                        lambda event: self.cd(event, contain[x][0]),
                    )
            if x + 1 < len(contain):
                container2 = wx.Panel(panel, -1, size=(90, 90), pos=(101, 5))
                container2.SetBackgroundColour("#8b8b8b")
                if contain[x + 1][2] == b"0":
                    container2.Bind(
                        wx.EVT_LEFT_UP,
                        lambda event: self.cd(event, contain[x + 1][0]),
                    )
                if contain[x + 1][2] == b"0":
                    image = wx.Image("ressource/image/folder.png").Scale(
                        60, 60, wx.IMAGE_QUALITY_HIGH
                    )
                elif contain[x + 1][2] == b"1":
                    image = wx.Image("ressource/image/file.png").Scale(
                        60, 60, wx.IMAGE_QUALITY_HIGH
                    )
                bitmap2 = wx.StaticBitmap(
                    container2,
                    -1,
                    image.ConvertToBitmap(),
                    size=(60, 60),
                    pos=(15, 10),
                )
                if contain[x + 1][2] == b"0":
                    bitmap2.Bind(
                        wx.EVT_LEFT_UP,
                        lambda event: self.cd(event, contain[x + 1][0]),
                    )
                label2 = wx.StaticText(
                    container2,
                    -1,
                    contain[x + 1][0],
                    size=(90, 20),
                    pos=(0, 70),
                    style=wx.ALIGN_CENTRE,
                )
                if contain[x + 1][2] == b"0":
                    label2.Bind(
                        wx.EVT_LEFT_UP,
                        lambda event: self.cd(event, contain[x + 1][0]),
                    )
            if x + 2 < len(contain):
                container3 = wx.Panel(panel, -1, size=(90, 90), pos=(197, 5))
                container3.SetBackgroundColour("#8b8b8b")
                if contain[x + 2][2] == b"0":
                    container3.Bind(
                        wx.EVT_LEFT_UP,
                        lambda event: self.cd(event, contain[x + 2][0]),
                    )
                if contain[x + 2][2] == b"0":
                    image = wx.Image("ressource/image/folder.png").Scale(
                        60, 60, wx.IMAGE_QUALITY_HIGH
                    )
                elif contain[x + 2][2] == b"1":
                    image = wx.Image("ressource/image/file.png").Scale(
                        60, 60, wx.IMAGE_QUALITY_HIGH
                    )
                bitmap3 = wx.StaticBitmap(
                    container3,
                    -1,
                    image.ConvertToBitmap(),
                    size=(60, 60),
                    pos=(15, 10),
                )
                if contain[x + 2][2] == b"0":
                    bitmap3.Bind(
                        wx.EVT_LEFT_UP,
                        lambda event: self.cd(event, contain[x + 2][0]),
                    )
                label3 = wx.StaticText(
                    container3,
                    -1,
                    contain[x + 2][0],
                    size=(90, 20),
                    pos=(0, 70),
                    style=wx.ALIGN_CENTRE,
                )
                if contain[x + 2][2] == b"0":
                    label3.Bind(
                        wx.EVT_LEFT_UP,
                        lambda event: self.cd(event, contain[x + 2][0]),
                    )
            if x + 3 < len(contain):
                container4 = wx.Panel(panel, -1, size=(90, 90), pos=(293, 5))
                container4.SetBackgroundColour("#8b8b8b")
                if contain[x + 3][2] == b"0":
                    container4.Bind(
                        wx.EVT_LEFT_UP,
                        lambda event: self.cd(event, contain[x + 3][0]),
                    )
                if contain[x + 3][2] == b"0":
                    image = wx.Image("ressource/image/folder.png").Scale(
                        60, 60, wx.IMAGE_QUALITY_HIGH
                    )
                elif contain[x + 3][2] == b"1":
                    image = wx.Image("ressource/image/file.png").Scale(
                        60, 60, wx.IMAGE_QUALITY_HIGH
                    )
                bitmap4 = wx.StaticBitmap(
                    container4,
                    -1,
                    image.ConvertToBitmap(),
                    size=(60, 60),
                    pos=(15, 10),
                )
                if contain[x + 3][2] == b"0":
                    bitmap4.Bind(
                        wx.EVT_LEFT_UP,
                        lambda event: self.cd(event, contain[x + 3][0]),
                    )
                label4 = wx.StaticText(
                    container4,
                    -1,
                    contain[x + 3][0],
                    size=(90, 20),
                    pos=(0, 70),
                    style=wx.ALIGN_CENTRE,
                )
                if contain[x + 3][2] == b"0":
                    label4.Bind(
                        wx.EVT_LEFT_UP,
                        lambda event: self.cd(event, contain[x + 3][0]),
                    )
            if x + 4 < len(contain):
                container5 = wx.Panel(panel, -1, size=(90, 90), pos=(389, 5))
                container5.SetBackgroundColour("#8b8b8b")
                if contain[x + 4][2] == b"0":
                    container5.Bind(
                        wx.EVT_LEFT_UP,
                        lambda event: self.cd(event, contain[x + 4][0]),
                    )
                if contain[x + 4][2] == b"0":
                    image = wx.Image("ressource/image/folder.png").Scale(
                        60, 60, wx.IMAGE_QUALITY_HIGH
                    )
                elif contain[x + 4][2] == b"1":
                    image = wx.Image("ressource/image/file.png").Scale(
                        60, 60, wx.IMAGE_QUALITY_HIGH
                    )
                bitmap5 = wx.StaticBitmap(
                    container5,
                    -1,
                    image.ConvertToBitmap(),
                    size=(60, 60),
                    pos=(15, 10),
                )
                if contain[x + 4][2] == b"0":
                    bitmap5.Bind(
                        wx.EVT_LEFT_UP,
                        lambda event: self.cd(event, contain[x + 4][0]),
                    )
                label5 = wx.StaticText(
                    container5,
                    -1,
                    contain[x + 4][0],
                    size=(90, 20),
                    pos=(0, 70),
                    style=wx.ALIGN_CENTRE,
                )
                if contain[x + 4][2] == b"0":
                    label5.Bind(
                        wx.EVT_LEFT_UP,
                        lambda event: self.cd(event, contain[x + 4][0]),
                    )
            bsizer.Add(panel, 0, wx.ALL, 5)

    def cd(self, event, dir):
        dir = dir.decode()
        # print(self.loc, dir)
        self.panel.Destroy()
        if dir == "..":
            if self.loc == "/":
                pass
            else:
                new_dir = self.loc.split("/")[-2]
                self.loc = self.loc[0 : len(self.loc) - len(new_dir) - 1]
                # if self.loc != "/":
                #    self.loc += "/"
                # print(self.loc)

        else:
            self.loc += dir + "/"
        self.draw()


class App(wx.App):
    def OnInit(self):
        frame = Frame(None, -1, "file explorer", self)
        frame.SetMaxSize(wx.Size(600, 500))
        frame.SetMinSize(wx.Size(600, 500))
        # frame.SetIcon(wx.Icon("/ressource/image/....png"))
        self.SetTopWindow(frame)
        frame.Show(True)
        return True


def main():
    app = App(0)
    app.MainLoop()


#

if __name__ == "__main__":
    main()
