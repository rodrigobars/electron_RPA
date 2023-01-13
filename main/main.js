const { app, BrowserWindow, ipcMain, screen  } = require('electron')
const { spawn } = require("child_process")
const path = require('path');

let win;
let newWindow

const createWindow = () => {
    win = new BrowserWindow({
        width: 440,
        height: 620,
        title: 'App-Uff',
        hasShadow: true,
        //alwaysOnTop: true,
        titleBarOverlay: false,
        resizable: false,
        transparent: true,
        frame:false,
        webPreferences: {
            contextIsolation: true,
            sandbox: true,
            preload: path.join(__dirname, 'preload.js'),
        },
    })
    let screenSize = screen.getPrimaryDisplay().workAreaSize;
    
    let x = 50;
    let y = (screenSize.height / 2) - (win.getSize()[1] / 2);

    win.setPosition(x, y);
    win.loadFile(path.join(__dirname, 'html/index.html'))

    win.on('move', () => {
        console.log('moving...')

        set_newWindow_Position()
    })

    //janela auxiliar
    newWindow = new BrowserWindow({
        width: 700,
        height: 490,
        parent: win,
        show: false,
        modal: false,
        titleBarOverlay: false,
        resizable: false,
        transparent: false,
        frame: false,
    });
}

app.whenReady().then(() => {
    createWindow();
    app.on('activate', () => {
        if (BrowserWindow.getAllWindows().length === 0) {
            createWindow();
    }
    });
});

app.on('window-all-closed', () => {
    if (process.platform !== 'darwin') {
        app.quit();
    }
});

let expanded = false
ipcMain.handle('expand_screen', () => {
    if (!expanded) {
        set_newWindow_Position()
        show()
        function f() {
            newWindow.show()
        }
        setTimeout(f, 800)
    }else{
        set_newWindow_Position()
        newWindow.hide()
        setTimeout(hide, 800)
    }
})

ipcMain.handle('close', () => {
    app.quit();
})

ipcMain.handle('minimize', () => {
    win.minimize();
})

ipcMain.handle('openMainPy', (event, num_pregao) => {

    set_newWindow_Position()

    //newWindow.loadURL("http://localhost:5000");
    newWindow.loadURL("http://google.com");
    newWindow.show();

    const pythonProcess = spawn('python', [path.join(__dirname, '/python/testeflask.py'), num_pregao])
    pythonProcess.stdout.on('data', (data) => {
        console.log(`stdout:\n ${data}`);
    });
    
    pythonProcess.stderr.on('data', (data) => {
        console.error(`stderr: ${data}`);
    });
    
    pythonProcess.on('close', (code) => {
        console.log(`child process exited with code ${code}`);
    });
})

function set_newWindow_Position() {
    let position = win.getPosition();
    let x = 440 + position[0] + 5
    let y = position[1] + 70;

    newWindow.setPosition(x, y);
}

function hide() {
    console.log('closing...')
    const { width, height } = win.getBounds()
    
    let currentWidth = width
    let step = 80
    const interval = setInterval(() => {
        if (currentWidth <= 440) {
            clearInterval(interval)
            return
        }
        currentWidth -= step
        win.setBounds({
            width: currentWidth,
            height: height
        })
    }, 15)
    expanded = false
}

function show() {
    console.log('Opening...')
    const { width, height } = win.getBounds()
    
    let targetWidth = (width * 3) - 100
    let currentWidth = width
    let step = 80
    const interval = setInterval(() => {
        if (currentWidth >= targetWidth) {
            clearInterval(interval)
            return
        }
        currentWidth += step
        win.setBounds({
            width: currentWidth,
            height: height
        })
    }, 15)
    expanded = true
}