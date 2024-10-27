

const uploadPic = async (req, res) => {
    try{
        const temp = (await user.find({'emailId': req.user.emailId}))[0]
        if(temp.profilePic == "NoProfilePic"){
            cloudinary.uploader.upload(req.file.path)
                .then(async (result) => {
                    const updates = {
                        profilePic: result.secure_url
                    }
                    await user.findOneAndUpdate({"emailId": req.user.emailId}, updates)
                    deleteFile(req.file.path)
                })
                .catch(() => {
                    console.log("Upload Failed")
                })
            return res.send(req.file)
        }
        else{
            deleteFile(req.file.path)
            return res.send("ProfilePic already exists !!")
        }
    }
    catch(err){
        console.log(err.message)
    }
}