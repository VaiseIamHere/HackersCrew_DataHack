const multer = require("multer")

const storage = multer.diskStorage({
  destination: "./upload",
  filename: (req, file, cb) => {
    const newname = `${Date.now()}_${file.originalname}`; // Corrected string interpolation
    cb(null, newname);
  }
});

const upload = multer({ storage: storage });

module.export = {
    upload
} // Export the upload middleware
