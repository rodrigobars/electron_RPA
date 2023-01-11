const { contextBridge, ipcRenderer } = require('electron')

// let a = 3
// let b = 4

contextBridge.exposeInMainWorld('call', {
    openMainPy: (num_pregao) => ipcRenderer.invoke("openMainPy", num_pregao),
    expand_screen: () => ipcRenderer.invoke('expand_screen'),
    close: () => ipcRenderer.invoke('close'),
    minimize: () => ipcRenderer.invoke('minimize')
})