async function shareHandler(e,id){
    try{
        const share = await axios.post('polls/share/'+id,{
            share:e.target.value,
        })
    }
    catch(error){
        console.log("error");
    }
}