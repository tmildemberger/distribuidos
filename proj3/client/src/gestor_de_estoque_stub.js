import * as grpc from '@grpc/grpc-js';
import * as protoLoader from '@grpc/proto-loader';

var PROTO_PATH = __dirname + '/gestor_de_estoque.proto';

// Suggested options for similarity to existing grpc.load behavior
var packageDefinition = protoLoader.loadSync(
    PROTO_PATH,
    {keepCase: true,
     longs: String,
     enums: String,
     defaults: true,
     oneofs: true
    });
var protoDescriptor = grpc.loadPackageDefinition(packageDefinition);
// The protoDescriptor object has the full package hierarchy
var gestor_de_estoque = protoDescriptor.gestor_de_estoque;
//console.log(gestor_de_estoque);
var stub = new gestor_de_estoque.GestorDeEstoque('localhost:50051', grpc.credentials.createInsecure());

export default stub;