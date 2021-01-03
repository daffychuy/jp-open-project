// Query Template
const JAP_TEMPLATE = {
	slug: "",
	is_common: false,
	tags: [],
	jlpt: [],
	Japanese: [],
	sense: [],
	attribution: {
		jmdict: false,
	},
};

// HTTP response status codes
const NOT_FOUND = 404,
	INVALID = 400,
	SUCCESS = 200,
	INTERNAL_ERROR = 500;
module.exports = {
	JAP_TEMPLATE,
	NOT_FOUND,
	INVALID,
	SUCCESS,
	INTERNAL_ERROR,
};
