const run = () => {
    const links = ['reject', 'accept']
    var urlParams = new URLSearchParams(window.location.search);
    chainType = urlParams.get('type')
    chainID = urlParams.get('id')

    updateTitle(chainType)

    console.log(chainType, chainID)

    updateImages(chainType, chainID)

    $('#btn-1').click(() => {
        reject(chainType, chainID)
            .then(() => {
                updateImages(chainType, chainID)
            })
    })

    $('#btn-2').click(() => {
        accept(chainType, chainID)
            .then(() => {
                updateImages(chainType, chainID)
            })
    })
}

const updateImages = (chainType, chainID) => {
    return getImageNames(chainType, chainID)
        .then((data) => {
            $('#img-1').attr('src', `images/${data.current}`)
            $('#img-2').attr('src', `images/${data.proposal}`)
            $('#steps').text(data.steps)
        })
}

const getImageNames = (chainType, chainID) => {
    // const Http = new XMLHttpRequest()
    const url = `http://127.0.0.1:5002/types/${chainType}/chains/${chainID}`
    // Http.open("GET", url)
    // Http.send()
    //
    // Http.onreadystatechange = () => {
    //
    // }
    return new Promise((resolve, reject) => {
        $.get(url, (data, status) => {
            console.log(data)
            resolve(data)
        })
    })
}

const accept = (chainType, chainID) => {
    const url = `http://127.0.0.1:5002/types/${chainType}/chains/${chainID}/accept`
    return new Promise((resolve, reject) => {
        $.get(url, (data, status) => {
            console.log(data)
            resolve(data)
        })
    })
}

const reject = (chainType, chainID) => {
    const url = `http://127.0.0.1:5002/types/${chainType}/chains/${chainID}/reject`
    return new Promise((resolve, reject) => {
        $.get(url, (data, status) => {
            console.log(data)
            resolve(data)
        })
    })
}

const updateTitle = (type) => {
    $('#title').text(`Which looks more like a ${type}`)
}

$(document).ready(run)