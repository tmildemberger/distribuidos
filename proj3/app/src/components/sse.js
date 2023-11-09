const _ = require('lodash');
 
  /**
   * The constructor.
   *
   * @param {Object} response
   * @param {Object} options
   * @return {SSE}
   * @constructor
   */
  function SSE(response, options) {
    if (!(this instanceof SSE)) {
      return new SSE(response, options);
    }
 
    options = _.defaults({}, options, {
      retry: 10000,
    });
 
    this.response = response;
 
    // This is the SSE header
    response.writeHead(200, {
      'Content-Type': 'text/event-stream',
      'Cache-Control': 'no-cache',
      'Access-Control-Allow-Origin': '*',
    });
 
    response.write(`:${Array(2049).join(' ')}\n`); // 2kB padding for IE
 
    // Set time before retry if connection error.
    // This need to be set before sending any message.
    response.write(`retry: ${options.retry}\n`);
  }
 
  /**
   * Send message.
   *
   * @param {*} id
   * @param {*} data
   */
  SSE.prototype.write = function (id, data) {
    this.response.write(`id: ${id}\n`);
    this.response.write(`data: ${data}\n\n`);
  };
 
  /**
   * End connection.
   *
   * @param {*} data
   */
  SSE.prototype.end = function (data) {
    this.response.write('event: result\n');
    this.response.write(`data: ${data}\n\n`);
    this.response.end();
  };
 
  module.exports = SSE;