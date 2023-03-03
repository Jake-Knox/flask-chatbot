


let createDiv = (message) =>{      
    // console.log(user)
    // console.log(message)
    // console.log(" ")
    const chatDiv = document.getElementById("chat-messages-div")
    
    // list of the script elements which spawn the messages
    let myArr = []
    myArr = document.getElementsByClassName("creator-script")
    //console.log(myArr.length)


    
    const newDiv = document.createElement("div")
    newDiv.classList = (`${message[0]}`)

    const userP =  document.createElement("p")
    userP.innerText = (`${message[0]}`)

    const messageP = document.createElement("p")
    messageP.classList = (`typing`)

    newDiv.append(userP)
    newDiv.append(messageP)
    chatDiv.append(newDiv)  


    // 0.05 seconds - 20 letters a second
    let timeBetweenLetter = 50 
    let lastChar = 0
    const typewriter = () => {
        setTimeout(() => {
            // console.log(message)
            if (lastChar == message[1].length) {
                return;
            }
            messageP.textContent += message[1][lastChar]    
            lastChar++;
            typewriter();
        }, timeBetweenLetter)
    }
    typewriter()

    // Scrolls to the bottom
    chatDiv.scrollTo(0, chatDiv.scrollHeight) 
}



// const startTimer = () => {
//     setInterval(myTimer, 1000);
//     function myTimer() 
//     {    
//         for (p in document.getElementsByClassName("typing"))
//         {
//             p.innerText += "."
//         }
//     }
//     myTimer()
// }

{/* <div class={{answer[0]}}>
    <p>{{answer[0]}}</p>
    <p class="typing">{{answer[1]}}</p>
</div>  */}