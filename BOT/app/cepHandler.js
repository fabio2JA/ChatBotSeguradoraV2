import axios from "axios";


export async function viewCepInfos(cep) {
    const url = `viacep.com.br/ws/${cep}/json/`
    axios.get(url, {
        headers: {
            'Content-Type': 'multipart/form-data'
        }
    }).then(response => {
        console.log(response.data);
    }).catch(error => {
        console.log(error);
    });
}