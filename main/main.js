const { app, BrowserWindow, ipcMain, screen  } = require('electron')
const { spawn } = require("child_process")
const path = require('path')

let win;
const createWindow = () => {
    win = new BrowserWindow({
        width: 440,
        height: 620,
        title: 'App-Uff',
        hasShadow: true,
        //alwaysOnTop: true,
        //darkTheme: true,
        //opacity: 0.95,
        titleBarOverlay: false,
        resizable: false,
        //titleBarStyle: "hidden",
        transparent: true,
        frame:false,
        webPreferences: {
            contextIsolation: true,
            sandbox: true,
            preload: path.join(__dirname, 'preload.js'),
        },
    })
    // Obtém as dimensões da tela atual
    let screenSize = screen.getPrimaryDisplay().workAreaSize;

    // Calcula as coordenadas x e y da janela
    //let x = (screenSize.width - win.getSize()[0]);
    let x = 50
    let y = (screenSize.height / 2) - (win.getSize()[1] / 2);

    // Modifica o posicionamento da janela
    win.setPosition(x, y);
    win.loadFile(path.join(__dirname, 'html/index.html'))
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
    console.log('Opening...')
    const { width, height } = win.getBounds()

    let targetWidth = (width * 3) - 100
    let currentWidth = width
    let step = 80

    if (!expanded) {
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
        }, 10)
        expanded = true
    }else{
        console.log('closing...')
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
})

ipcMain.handle('close', () => {
    app.quit();
})

ipcMain.handle('minimize', () => {
    win.minimize();
})

ipcMain.handle('openMainPy', (event, num_pregao) => {
    const pythonProcess = spawn('python', [path.join(__dirname, '/python/main.py'), num_pregao])
    pythonProcess.stdout.on('data', (data) => {
        console.log(`stdout: ${data}`);
    });
    
    pythonProcess.stderr.on('data', (data) => {
        console.error(`stderr: ${data}`);
    });
    
    pythonProcess.on('close', (code) => {
        console.log(`child process exited with code ${code}`);
    });
})