NODE_MODULES=./node_modules
JS_SENTINAL=$(NODE_MODULES)/sentinal
JSHINT=$(NODE_MODULES)/jshint/bin/jshint
JSCS=$(NODE_MODULES)/jscs/bin/jscs
WEBPACK=$(NODE_MODULES)/.bin/webpack
WEBPACK_CONFIG=webpack.config.js
WP_SENTINAL=media/dist/sentinal

jshint: $(JS_SENTINAL)
	$(JSHINT) $(JS_FILES)

jscs: $(JS_SENTINAL)
	$(JSCS) $(JS_FILES)

$(JS_SENTINAL): package.json
	rm -rf $(NODE_MODULES)
	npm install
	touch $(JS_SENTINAL)
