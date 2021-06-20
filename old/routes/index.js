import { Router } from "express";
const router = Router({ mergeParams: true, strict: false });

/* Redirect to API request file */
router.use("/search", require("./search"));

/* GET home page. */
router.get("/", function (req, res) {
	res.render("index", { title: "Express" });
});

export default router;
